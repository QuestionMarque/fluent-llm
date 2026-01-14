"""Stub functions representing the LLM planning layer.

In the real system, a large language model would take a natural language
description of a task and produce a structured IRJob.  Here we
implement a very simple parser that recognizes a few key phrases and
generates corresponding IR steps.  It is intended only to illustrate
how the LLM might interface with the rest of the system.

TODO: Replace this stub with a proper integration using OpenAI's
functions or another model capable of producing JSON in the expected
schema.  Refer to the design in phase 3 for error repair loops and
tool‑calling patterns.
"""

import re
from typing import Tuple
from .ir import IRJob, IRStep


def plan_from_text(task_description: str) -> IRJob:
    """Convert a task description into a simple IRJob.

    Supports phrases like "transfer X uL from Plate S1 A1 to Plate D1 B1",
    "wash", and "decontaminate".  Unknown phrases are ignored.

    Args:
        task_description: The natural language description from the user.

    Returns:
        An IRJob containing one or more IRSteps.  Job metadata is
        generated automatically.
    """
    steps = []
    # Example pattern: "transfer 50 uL from plate S1 A1 to plate D1 B1"
    transfer_pattern = re.compile(r"transfer\s+(\d+(?:\.\d+)?)\s*u?l\s+from\s+plate\s+(\w+)\s+(\w+)\s+to\s+plate\s+(\w+)\s+(\w+)", re.IGNORECASE)
    for match in transfer_pattern.finditer(task_description):
        vol = float(match.group(1))
        src_labware = match.group(2)
        src_well = match.group(3)
        dest_labware = match.group(4)
        dest_well = match.group(5)
        step_id = f"s{len(steps)+1}"
        steps.append(IRStep(
            id=step_id,
            op="transfer",
            args={
                "source_labware": src_labware,
                "source_well": src_well,
                "dest_labware": dest_labware,
                "dest_well": dest_well,
                "volume_uL": vol
            },
            preconditions=["robot.homed == true", "tip.attached == true"]
        ))
    # Detect wash
    if re.search(r"wash", task_description, re.IGNORECASE):
        step_id = f"s{len(steps)+1}"
        steps.append(IRStep(id=step_id, op="wash", args={"scheme": 1}, preconditions=["robot.homed == true"]))
    # Detect decontaminate
    if re.search(r"decontaminat", task_description, re.IGNORECASE):
        step_id = f"s{len(steps)+1}"
        steps.append(IRStep(id=step_id, op="decontaminate", args={}, preconditions=["robot.homed == true"]))
    # Build IRJob
    job_id = "job" + str(abs(hash(task_description)) % 100000)
    return IRJob(version="1.0", job_id=job_id, name=task_description, steps=steps, constraints={"require_homed": True})