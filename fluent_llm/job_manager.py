"""JobManager orchestrates the lifecycle of IR jobs.

The manager maintains a queue of submitted jobs, performs preflight
validation, compiles jobs into worklists, simulates them (as a dry run),
and (in a real deployment) would dispatch compiled worklists to the
robot control interface.  For this prototype, execution is simulated.

TODO: Add support for pausing, resuming, aborting jobs, concurrency
control, and integrating with a real Fluent control API.
"""

from typing import List
from .ir import IRJob
from .preflight import preflight_check
from .compiler import compile_ir
from .simulator import simulate_ir
from .state import ErrorType, RecoveryAction


class JobManager:
    """Simple job orchestrator.

    Attributes:
        deck_state: A mapping of labware names to metadata (e.g. positions).
        queue: FIFO list of IR jobs awaiting execution.
        error_policy: Mapping of ErrorType to RecoveryAction.  Determines what
            to do when preflight or execution errors occur.
    """

    def __init__(self, deck_state=None):
        self.deck_state = deck_state or {}
        self.queue: List[IRJob] = []
        # Default policy: abort on any error
        self.error_policy = {
            ErrorType.LABWARE_NOT_FOUND: RecoveryAction.ABORT,
            ErrorType.VOLUME_OUT_OF_RANGE: RecoveryAction.ABORT,
            ErrorType.UNKNOWN_OPERATION: RecoveryAction.ABORT,
            ErrorType.PRECONDITION_FAILED: RecoveryAction.ABORT,
            ErrorType.TIP_NOT_AVAILABLE: RecoveryAction.ABORT,
            ErrorType.MOTION_ERROR: RecoveryAction.ABORT,
        }

    def submit(self, job: IRJob):
        """Add a job to the queue after running preflight validation.

        If validation fails, the job is not enqueued and a ValueError is
        raised.  In a real system, you might instead place the job in a
        'validation failed' state and allow user correction.
        """
        errors = preflight_check(job, self.deck_state)
        if errors:
            messages = [f"{step_id}: {error.name} – {msg}" for step_id, error, msg in errors]
            raise ValueError("Preflight check failed:\n" + "\n".join(messages))
        self.queue.append(job)

    def run_next(self):
        """Compile and simulate the next job in the queue.

        Returns:
            A tuple (worklist_lines, simulation_state) where worklist_lines is
            a list of strings representing the compiled worklist and
            simulation_state is a dict of labware volumes after simulation.

        Raises:
            IndexError: If no jobs are queued.
        """
        if not self.queue:
            raise IndexError("No jobs queued")
        job = self.queue.pop(0)
        # Compile
        worklist_lines = compile_ir(job)
        # Simulate execution
        sim_state = simulate_ir(job)
        return worklist_lines, sim_state