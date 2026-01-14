"""Intermediate representation (IR) definitions.

The IR is a robot‑agnostic description of tasks expressed as a sequence of
steps with explicit parameters and preconditions.  A version field at
the job level allows for evolution of the schema over time.

TODO: Extend the IR to cover all operations supported by the robot,
including mixing, pooling, gripper moves, and custom liquid classes.  See
Tecan's worklist command documentation for a complete list of
record types【6713682743180†L32-L40】.
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class IRStep:
    """A single step in an IR job.

    Attributes:
        id: A unique identifier for the step.
        op: The operation to perform (e.g., "transfer", "wash", "decontaminate").
        args: A dictionary of operation‑specific arguments.
        preconditions: A list of expressions that must evaluate to True before
            the step can be executed.  These expressions refer to robot state
            variables (e.g. 'robot.homed == true', 'tip.attached == true').

    The set of allowed operations and their expected arguments should be
    synchronized with the compiler module.  Unknown operations will cause
    compilation to fail.
    """

    id: str
    op: str
    args: Dict[str, Any] = field(default_factory=dict)
    preconditions: List[str] = field(default_factory=list)


@dataclass
class IRJob:
    """A collection of IR steps along with job‑level metadata.

    Attributes:
        version: Version of the IR schema.  Increment when making breaking
            changes to the schema.
        job_id: A unique identifier for the job.
        name: An optional human readable name.
        steps: Ordered list of IRStep objects.
        constraints: Arbitrary job‑level constraints (e.g. speed limits,
            collision avoidance).  The compiler may ignore constraints it
            doesn't understand.
    """

    version: str
    job_id: str
    name: Optional[str] = None
    steps: List[IRStep] = field(default_factory=list)
    constraints: Dict[str, Any] = field(default_factory=dict)