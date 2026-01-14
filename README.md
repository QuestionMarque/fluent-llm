# fluent_robot

`fluent_robot` is a prototype Python package for translating high‑level, natural‑language descriptions of liquid‑handling tasks into **Tecan Fluent** worklist files.  The package defines an intermediate representation (IR) that captures tasks in a robot‑agnostic way, validates the IR against basic constraints, compiles it into `.gwl` worklists, and simulates the resulting liquid transfers.  It also includes a simple stub for integrating with a large language model (LLM) that converts plain English instructions into IR.  This repository accompanies the project report describing the phases of the design and is intended for exploration and learning rather than production deployment.

## Repository structure

| Path | Purpose |
| ---- | ------- |
| **fluent_robot/** | The Python package implementing the IR, compiler, validator, simulator and job manager. |
| `fluent_robot/__init__.py` | Exports top‑level classes and functions so they can be imported directly from `fluent_robot`. |
| `fluent_robot/ir.py` | Dataclasses that define the intermediate representation (IR) for jobs and steps. |
| `fluent_robot/compiler.py` | Translates IR steps into Gemini WorkList (`.gwl`) record lines.  Supports `transfer`, `wash` and `decontaminate` operations. |
| `fluent_robot/preflight.py` | Performs simple preflight validation on IR jobs (e.g., labware exists, volumes in range). |
| `fluent_robot/simulator.py` | Provides a minimal dry‑run simulator that updates virtual plate volumes. |
| `fluent_robot/job_manager.py` | Orchestrates job submission, validation, compilation and simulation.  Meant to be extended to talk to a real robot. |
| `fluent_robot/state.py` | Error and recovery action definitions used by the validator and job manager. |
| `fluent_robot/llm_stub.py` | A very basic parser that interprets transfer, wash and decontamination requests from free text into IR steps. |
| `fluent_robot/capabilities.yaml` | YAML registry enumerating supported operations (aspirate, dispense, wash, decontaminate) and global constraints such as volume limits.  This file is a placeholder; expand it using the Fluent documentation during Phase 1. |
| `fluent_robot/capabilities.py` | Loader that reads the YAML registry and returns a Python dictionary via `get_capabilities()`.  This allows validators and compilers to look up available operations and constraints. |
| **tests/** | Unit tests covering the compiler, preflight validator, simulator and LLM stub.  Run them with `python3 -m unittest discover -v`. |
| `tests/test_capabilities.py` | Tests for the capability loader ensuring the registry loads correctly and that missing files return an empty dictionary. |
| **main.py** | Example script demonstrating the end‑to‑end flow: parse a natural‑language description, generate an IR job, validate it, compile it into a worklist, and simulate the result. |
| **project_phases.md** | A 2–3 page document outlining the project phases and explaining the design philosophy with citations to Fluent documentation. |
| **code_architecture.png** | Block diagram illustrating how the major components interact.  Used in the report. |
| **project_phases.docx** | Word version of the project report, generated from `project_phases.md`. |
| **fluent_robot_with_tests.zip** | Zipped archive containing the package, tests and example script for easy download. |

## Getting started

The package is self‑contained and has no external dependencies beyond the Python standard library.  You will need Python 3.8 or later.  To see the workflow in action:

```bash
python3 main.py
```

This will parse a sample instruction, compile a corresponding `.gwl` worklist, and perform a simple simulation of the transfer.

To run the unit tests:

```bash
python3 -m unittest discover -v
```

## License

This repository is provided for educational purposes as part of a project demonstration.  It is not licensed for production use.  Consult the manufacturer’s documentation and safety guidelines before deploying any code that drives laboratory hardware.