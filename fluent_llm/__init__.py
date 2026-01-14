"""fluent_llm package

This package provides a minimal framework for translating high‑level
intermediate representation (IR) commands into Tecan Fluent control worklist
commands (.gwl files), simulating execution, and orchestrating jobs.

The package is intended as a starting point for building more robust
integrations. Many functions are stubs or simplified to illustrate the
architecture. Each module contains TODO comments indicating where
additional functionality and validation against the FluentControl
documentation should be implemented.

Modules:

* ir – dataclasses describing the intermediate representation.
* compiler – functions to compile IR steps into .gwl lines.
* simulator – a simple simulation framework for dry‑runs.
* state – definitions of robot state and error handling.
* preflight – validation logic applied before compilation and execution.
* job_manager – orchestration of job submission, compilation and execution.
* llm_stub – stub functions representing the LLM planner interface.

Note: This code is intended for demonstration and prototyping purposes only.
It is not production ready.  Consult the FluentControl documentation and
robot manufacturer safety guidelines before deploying on real hardware.
"""

from .ir import IRJob, IRStep
from .compiler import compile_ir
from .simulator import simulate_ir
from .preflight import preflight_check
from .job_manager import JobManager
from .llm_stub import plan_from_text
from .capabilities import get_capabilities  # expose capabilities loader
from .api import RobotAPI  # API façade for robot control
from .policy import classify_step, is_allowed  # risk classification helpers
from .llm_integration import generate_ir_from_text, repair_ir_job  # LLM planning utilities