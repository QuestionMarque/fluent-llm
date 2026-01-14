# LLM‑Driven Fluent Control Project: Phases and Code Architecture

This document summarizes the key phases of the project to enable natural‑language control of a Tecan Fluent liquid‑handling robot.  It is intended for new engineering team members who need to understand both the project plan and how the accompanying Python package is structured.  Citations point back to the Fluent documentation for record structures and worklist behaviour.

## Phase 1 – Contracts & Models

The first phase establishes a **shared contract** between the AI planner and the robot.  Without clear contracts, later steps become guesswork and unsafe.  You will:

1. **Enumerate capabilities and constraints.**  Fluent worklists consist of seven record types (Aspirate, Dispense, Wash tips / Replace DiTis, Flush, Break, Set DiTi Type and Comment)【6713682743180†L32-L40】.  Each record begins with a single character (`A`, `D`, `W`, `F`, `B`, `S`, `C`) and is followed by semicolon‑separated parameters【6713682743180†L32-L40】.  Document the required and optional parameters for each record and capture physical limits (e.g. volume ranges, tip capacities, labware types).

2. **Define the intermediate representation (IR).**  The IR is a robot‑agnostic schema that describes *what* needs to be done.  It includes the job version, job ID, a list of steps, and job‑level constraints.  Each step has an identifier, an operation (`op`), arguments (`args`) and preconditions.  Our `fluent_robot/ir.py` module defines these dataclasses.  For example:

```python
from fluent_robot.ir import IRJob, IRStep

job = IRJob(
    version="1.0",
    job_id="example",
    name="Example transfer",
    steps=[
        IRStep(id="s1", op="transfer", args={
            "source_labware": "S1",
            "source_well": "A1",
            "dest_labware": "D1",
            "dest_well": "B1",
            "volume_uL": 50.0
        }, preconditions=["robot.homed == true", "tip.attached == true"])
    ],
    constraints={"require_homed": True}
)
```

3. **Establish an error taxonomy.**  Identify error conditions such as labware not found, volume out of range, unknown operations, etc.  The preflight validator uses these to detect problems before execution.

### Data Required from Fluent Documentation

To implement Phase 1 correctly you must extract from the official Fluent documentation:

* **Record parameter definitions** – what each field after the record type means and its valid values.  For example, the documentation shows that an aspirate record has parameters `RackLabel;RackID;RackType;Position;TubeID;Volume;LiquidClass;TipType;TipMask;ForcedRackType`【6713682743180†L56-L59】.  Without these definitions you cannot map IR arguments to worklist fields.
* **Well numbering scheme** – numeric positions are computed by counting eight rows per column (A2 becomes position 9)【6713682743180†L91-L97】.
* **Volume and tip limits** – maximum and minimum volumes per tip type and labware, along with allowed liquid classes and wash schemes.
* **Error and warning behaviour** – FluentControl defines how to handle missing labware (skip, warn, stop)【654457521633302†L112-L124】.  These behaviours must be mirrored in the preflight validator and job manager.

## Phase 2 – Deterministic Execution

Once the contracts are defined, Phase 2 builds a **deterministic execution layer**.  This layer converts IR into a Tecan worklist and provides a dry‑run capability.

1. **Compiler:**  The `fluent_robot/compiler.py` module implements `compile_ir(job)` to translate each IR step into one or more `.gwl` lines.  For a transfer step it produces an `A` record (aspirate) and a `D` record (dispense).  It uses the helper `well_to_position()` to convert alphanumeric wells (A1–H12) into numeric positions; this function multiplies the column index by eight and adds the row index + 1, so `A2` becomes position 9【6713682743180†L91-L97】.  The compiler currently supports three operations:
   * **transfer:** Generates `A` and `D` records with the specified labware, well positions and volume.
   * **wash:** Generates `W<scheme>;` lines.  The default scheme is 1, but the manual defines multiple wash schemes that you should enumerate.
   * **decontaminate:** Generates `WD;`, which performs a decontamination wash【246479156155221†L123-L125】.

   The compiler is deliberately conservative: unknown operations result in a failure.  Many advanced commands (flush `F;`, break `B;`, set DiTi type `S;`) and additional parameters (e.g. liquid class, tip mask) are marked as TODOs.  They should be implemented once the necessary data is extracted from the manual【246479156155221†L96-L131】.

2. **Preflight validator:**  Before compilation, `preflight_check(job, deck_state)` verifies that referenced labware exists, that volumes are within bounds, and that the operations are known.  It returns a list of errors; the job manager rejects jobs that fail.  In a future iteration the validator will perform context checks similar to FluentControl (e.g. skip vs. warn vs. error for missing labware【654457521633302†L112-L124】).

3. **Simulator:**  The `fluent_robot/simulator.py` module provides a minimal dry‑run.  It tracks volumes in 96‑well plates and updates them according to transfer operations.  Wash and decontamination are logged but do not change state.  Real physical limits (e.g. 250 µL per well) and mixing behaviour are not modelled; consult the documentation and libraries like `robotools` to extend the simulator【189890760946635†L45-L100】.

4. **Job manager:**  `fluent_robot/job_manager.py` orchestrates the process.  It holds a queue of IR jobs, runs preflight checks, compiles the worklists, simulates them and would, in a production system, dispatch them to the robot.  Recovery actions for different error types (abort, skip, retry) are configurable.

### Data Required from Fluent Documentation

* **Advanced command parameters** – `W` (wash), `WD` (decontaminate), `F` (flush), `B` (break), `S` (set DiTi type) and `R` (reagent distribution) each have specific parameter sets and side effects.  For example, `WD` performs a decontamination wash for fixed tips only【246479156155221†L123-L125】.  The manual should specify the allowed schemes (W1, W2, etc.), the meaning of each parameter and when commands can be used.
* **Liquid class precedence** – In advanced worklists the liquid class defined in the file overrides the script’s liquid class【246479156155221†L135-L139】.  The compiler must honour this rule.
* **Tip handling rules** – How to handle multiple tips, tip masks, dynamic tip handling and mixing commands.  Currently the compiler sets unspecified fields blank; you need to fill them according to the manual.

## Phase 3 – Safety & AI Integration (preview)

Phase 3 introduces the AI planner and safety policies.  Although your task focuses on phases 1–2, it is important to understand how they fit into the larger system:

* **LLM planner:**  A large language model converts user instructions into IR.  Our `fluent_robot/llm_stub.py` file contains a rudimentary parser that extracts transfer commands, wash and decontamination requests from free text.  In production this will be replaced by an LLM that emits JSON IR objects and handles validation errors via a repair loop.
* **Safety policies:**  Preflight checks will incorporate risk classification (allow / confirm / block) and enforce permissioning.  For example, decontamination may require operator confirmation.
* **Tool API (MCP):**  The robot API will be wrapped as a set of tools (e.g. `submit_job`, `validate_plan`, `get_state`), allowing the LLM to call them reliably.

## Code Architecture Diagram

The Python package mirrors the phased architecture.  The diagram below illustrates how the major sub‑systems interact:

![Code Architecture]({{file:file-K6XFceuW5corfZmPTsC5r7}})

* **LLM Planner (stub)** – Parses natural language into an IR job (Phase 3).  In this project we include only a stub for testing.
* **IR (Data Models)** – Defines the job and step schemas used throughout the system.
* **Preflight Validator** – Validates IR jobs against the deck state and policy (Phase 2).
* **Compiler** – Converts validated IR into `.gwl` lines (Phase 2).  This module is the primary consumer of Fluent documentation.
* **Job Manager** – Manages submission, queuing, compilation, simulation and (in a full system) execution (Phase 2/3).
* **Simulator** – Performs dry‑runs by updating volumes in virtual labware (Phase 2).  Useful for testing and debugging.

## Running the Example Workflow

To see these components in action, run the included `main.py` script.  It demonstrates how a natural‑language description is transformed into a worklist and simulated:

```bash
python3 main.py
```

You should see output similar to:

```
Task description: Transfer 50 uL from plate S1 A1 to plate D1 B1, wash, then decontaminate.

Generated IR job:
  s1 – op=transfer, args={...}
  s2 – op=wash, args={'scheme': 1}
  s3 – op=decontaminate, args={}

Compiled worklist lines:

A;S1;;;1;;50.00;Water;;;
D;D1;;;2;;50.00;Water;;;
W1;
WD;

Simulation state (delta volumes):
  S1: total volume = -50.0 µL
  D1: total volume = 50.0 µL
```

This proves the pipeline works end‑to‑end for a simple scenario.  To extend it, implement additional commands and validations according to the Fluent documentation.