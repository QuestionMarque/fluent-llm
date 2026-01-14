"""Integration layer for natural language planning using an LLM.

This module builds on the simple parser in ``llm_stub.py`` to provide
structured functions for generating IR jobs from natural language
descriptions and repairing invalid plans.  In production, these
functions would call a large language model with properly engineered
prompts and tool definitions, then process the JSON output.  The
repair loop would feed back validation errors to the LLM until a
correct plan is produced or a maximum number of attempts is reached.
"""

from __future__ import annotations

from typing import List, Tuple

from .llm_stub import plan_from_text
from .ir import IRJob
from .state import ErrorType
from .preflight import preflight_check


def generate_ir_from_text(description: str, deck_state=None) -> IRJob:
    """Generate an IR job from a natural language description.

    Args:
        description: The user's task description in plain English.
        deck_state: Optional map of labware present on the deck.  If
            provided, the resulting IR job is validated against this
            state using :func:`preflight_check`.  Invalid plans
            trigger a repair loop.

    Returns:
        A validated IRJob.  If the repair loop fails to produce a
        valid plan within the allowed attempts, a ValueError is raised.

    TODO: Replace the call to :func:`plan_from_text` with a call to
    an actual LLM and incorporate tool calling instructions.  Provide
    context on robot capabilities and labware definitions to improve
    plan quality.
    """
    # Initial plan using the stub
    ir_job = plan_from_text(description)
    if deck_state is None:
        return ir_job
    # Validate and repair if necessary
    for attempt in range(3):
        errors = preflight_check(ir_job, deck_state)
        if not errors:
            return ir_job
        # For now, just raise after first failure – real implementation
        # would feed error messages back to the LLM and retry
        error_msgs = [f"{sid}: {err.name} – {msg}" for sid, err, msg in errors]
        raise ValueError("IR generation failed: " + "; ".join(error_msgs))
    raise ValueError("Unable to generate a valid IR plan after multiple attempts")


def repair_ir_job(ir_job: IRJob, errors: List[Tuple[str, ErrorType, str]], description: str) -> IRJob:
    """Placeholder for a plan repair function.

    Given a set of validation errors for an IR job, this function would
    construct a new prompt to the LLM requesting a corrected plan.
    Currently, it simply raises a ValueError to indicate that manual
    intervention is required.

    Args:
        ir_job: The invalid IR job.
        errors: A list of validation errors from :func:`preflight_check`.
        description: The original natural language description.

    Raises:
        ValueError: Always, since there is no repair logic implemented.
    """
    raise ValueError("Repair loop not implemented for IR job: errors=" + str(errors))
