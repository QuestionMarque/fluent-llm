"""Definitions of robot states and error handling.

This module defines a simple taxonomy of errors and states used by the
simulation and job manager.  The taxonomy should be expanded to match
the error codes and warnings documented in the FluentControl software
manual【654457521633302†L112-L124】.
"""

from dataclasses import dataclass
from enum import Enum
from typing import Optional


class ErrorType(Enum):
    """Enumerated error types.

    Additional error types should be added to mirror the full range of
    FluentControl errors (e.g., pipetting errors, tip collisions, barcode
    mismatches).  Each error type can be mapped to a recommended
    recovery action in the job manager.
    """

    LABWARE_NOT_FOUND = "labware_not_found"
    VOLUME_OUT_OF_RANGE = "volume_out_of_range"
    TIP_NOT_AVAILABLE = "tip_not_available"
    MOTION_ERROR = "motion_error"
    UNKNOWN_OPERATION = "unknown_operation"
    PRECONDITION_FAILED = "precondition_failed"


class RecoveryAction(Enum):
    """Recovery actions to take when encountering specific errors."""

    RETRY = "retry"
    SKIP = "skip"
    ABORT = "abort"
    REQUIRE_USER = "require_user"


@dataclass
class RobotEvent:
    """Represents a single event in the robot's execution timeline."""
    state: str
    error_type: Optional[ErrorType] = None
    message: Optional[str] = None