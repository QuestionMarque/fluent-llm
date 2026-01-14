"""Risk classification and safety policy definitions.

This module encapsulates the logic for classifying robot operations
according to risk and enforcing high‑level safety policies.  It
supplements the basic preflight validation with semantic rules such as
operator permissions, confirm‑required actions and hard‑blocked
operations.  Refer to Phase 5 of the project plan for guidance on how
to evolve this module.

For now, the risk classifications are simple mappings defined in
``RISK_POLICY``.  The default categories are:

* ``allow`` – the operation is considered safe and can execute
  automatically.
* ``confirm`` – the operation is allowed but requires explicit user
  confirmation (e.g. high‑volume transfers, decontamination).
* ``block`` – the operation is disallowed in the current context.  The
  job manager should abort or reject jobs containing blocked steps.

In addition to classifying operations, this module can be extended to
check user roles and permissions, enforce rate limits, and interface
with external risk engines.
"""

from __future__ import annotations

from typing import Dict

from .ir import IRStep


RISK_POLICY: Dict[str, str] = {
    "transfer": "allow",
    "wash": "allow",
    "decontaminate": "confirm",
    # Unknown operations are blocked by default
}


def classify_step(step: IRStep) -> str:
    """Return the risk classification for a given IR step.

    Args:
        step: The IR step to classify.

    Returns:
        One of ``"allow"``, ``"confirm"`` or ``"block"``.

    TODO: Extend this function to consider arguments (e.g. volume
    thresholds), user roles, and dynamic safety policies.  For
    example, transfers above 1000 µL might require confirmation.
    """
    return RISK_POLICY.get(step.op, "block")


def is_allowed(step: IRStep) -> bool:
    """Determine whether a step can proceed without confirmation.

    Returns ``True`` for ``allow`` steps, ``False`` for ``confirm`` and
    ``block`` steps.  For ``confirm`` steps, the user interface must
    prompt the operator before proceeding.  Blocked steps should not
    execute.
    """
    return classify_step(step) == "allow"
