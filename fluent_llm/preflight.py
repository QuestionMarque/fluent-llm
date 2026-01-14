"""Preflight validation for IR jobs.

Before compiling an IR job into a worklist and sending it to the robot,
perform basic validation to catch obvious issues such as missing labware
labels, volumes that exceed the instrument's limits, and unknown
operations.  This module only implements simple checks.  For
production use, extend the validator to inspect the actual deck setup
and enforce all safety policies defined in phase 3.
"""

from typing import Dict, List, Tuple
from .ir import IRJob, IRStep
from .state import ErrorType


def preflight_check(job: IRJob, deck_state: Dict[str, any], max_volume_uL: float = 1000.0) -> List[Tuple[str, ErrorType, str]]:
    """Validate an IR job against simple criteria.

    Args:
        job: The IR job to validate.
        deck_state: A mapping of labware names to metadata (e.g. positions,
            capacities).  For this prototype, deck_state is assumed to be a
            dictionary of present labware labels.
        max_volume_uL: Maximum volume in microliters allowed per aspirate or
            dispense.

    Returns:
        A list of tuples (step_id, error_type, message) for each validation
        failure detected.  An empty list means the job passed validation.

    TODO: Incorporate detailed labware dimensions, tip capacities, and
    user‑configured safety policies.  Refer to the Fluent worklist
    specification for required fields【6713682743180†L32-L40】 and to the
    preflight options described in the knowledge portal【654457521633302†L112-L124】.
    """

    errors: List[Tuple[str, ErrorType, str]] = []
    for step in job.steps:
        # Unknown operation check
        if step.op not in {"transfer", "wash", "decontaminate"}:
            errors.append((step.id, ErrorType.UNKNOWN_OPERATION, f"Unknown op: {step.op}"))
            continue

        # Common argument checks
        if step.op == "transfer":
            src_labware = step.args.get("source_labware")
            dest_labware = step.args.get("dest_labware")
            volume = step.args.get("volume_uL")
            if src_labware not in deck_state:
                errors.append((step.id, ErrorType.LABWARE_NOT_FOUND, f"Source labware {src_labware} missing"))
            if dest_labware not in deck_state:
                errors.append((step.id, ErrorType.LABWARE_NOT_FOUND, f"Destination labware {dest_labware} missing"))
            if volume is None or volume <= 0 or volume > max_volume_uL:
                errors.append((step.id, ErrorType.VOLUME_OUT_OF_RANGE, f"Volume {volume}µL invalid"))
        # Additional checks for wash and decontaminate could verify scheme ranges
        # or required equipment.  Currently, no arguments are mandatory.
    return errors