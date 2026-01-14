"""Simple simulator for dry‑running IR jobs.

The simulator tracks liquid volumes in labware wells and updates them
based on transfer operations.  It is intended for testing and does not
model physical dynamics such as blowout, tip mixing, or speed.  Wash and
decontamination operations are logged but do not modify state.

TODO: Integrate with a richer simulation framework (e.g. robotools)
to account for constraints like minimum/maximum volumes, tip usage,
mixing cycles and multi‑pipetting【189890760946635†L45-L100】.
"""

from typing import Dict, List
from .ir import IRJob
from .compiler import well_to_position


def simulate_ir(job: IRJob, initial_state: Dict[str, List[float]] = None) -> Dict[str, List[float]]:
    """Simulate the execution of an IR job on labware volumes.

    Args:
        job: The IR job to simulate.
        initial_state: Optional initial volumes for each labware.  The state
            should map labware labels to a list of 96 float values (µL).
            If not provided, all volumes start at 0 µL.

    Returns:
        A state dictionary mapping labware labels to updated volumes.

    Notes:
        This simulation assumes all wells can hold unlimited volume and does
        not enforce physical constraints.  In practice, each well has a
        maximum capacity (e.g. 250 µL for a 96‑well plate)【189890760946635†L45-L100】.
        Use the simulator only for quick sanity checks.
    """
    state: Dict[str, List[float]] = {}
    # Initialize state
    if initial_state is not None:
        for labware, volumes in initial_state.items():
            state[labware] = volumes.copy()
    # Ensure all labware in job appears in state
    for step in job.steps:
        if step.op == "transfer":
            for labware_key in (step.args.get("source_labware"), step.args.get("dest_labware")):
                if labware_key and labware_key not in state:
                    state[labware_key] = [0.0] * 96
        elif step.op in {"wash", "decontaminate"}:
            # wash/decontaminate does not require labware volumes
            continue

    # Simulate each step
    for step in job.steps:
        if step.op == "transfer":
            src_labware = step.args["source_labware"]
            src_well = step.args["source_well"]
            dest_labware = step.args["dest_labware"]
            dest_well = step.args["dest_well"]
            vol = step.args["volume_uL"]
            src_index = well_to_position(src_well) - 1
            dest_index = well_to_position(dest_well) - 1
            # Deduct volume from source and add to destination
            state[src_labware][src_index] -= vol
            state[dest_labware][dest_index] += vol
        elif step.op == "wash":
            # Placeholder: no state changes
            pass
        elif step.op == "decontaminate":
            # Placeholder: no state changes
            pass
    return state