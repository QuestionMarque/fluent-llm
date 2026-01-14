"""JobManager orchestrates the lifecycle of IR jobs.

The manager maintains a queue of submitted jobs, performs preflight
validation, compiles jobs into worklists, simulates them (as a dry run),
and (in a real deployment) would dispatch compiled worklists to the
robot control interface.  For this prototype, execution is simulated.

TODO: Add support for pausing, resuming, aborting jobs, concurrency
control, and integrating with a real Fluent control API.
"""

from typing import List, Dict, Any, Optional
from .ir import IRJob
from .preflight import preflight_check
from .compiler import compile_ir
from .simulator import simulate_ir
from .state import ErrorType, RecoveryAction


class JobManager:
    """Simple job orchestrator.

    The manager accepts IR jobs, performs preflight validation, and enqueues
    them for deterministic execution.  It maintains a minimal notion of job
    status (e.g. ``pending``, ``running``, ``paused``, ``completed``,
    ``aborted``, ``error``) and exposes methods for pausing, resuming and
    aborting jobs.  In this prototype, execution and status transitions are
    simulated; in a real system they would reflect the actual robot state.

    Attributes:
        deck_state: A mapping of labware names to metadata (e.g. positions).
        queue: FIFO list of IR jobs awaiting execution.
        job_status: Mapping of job IDs to status strings.
        error_policy: Mapping of ErrorType to RecoveryAction.  Determines what
            to do when preflight or execution errors occur.
    """

    def __init__(self, deck_state=None):
        self.deck_state = deck_state or {}
        self.queue: List[IRJob] = []
        # Track job statuses keyed by job_id. New jobs are "pending" until run.
        self.job_status: Dict[str, str] = {}
        # Default policy: abort on any error
        self.error_policy = {
            ErrorType.LABWARE_NOT_FOUND: RecoveryAction.ABORT,
            ErrorType.VOLUME_OUT_OF_RANGE: RecoveryAction.ABORT,
            ErrorType.UNKNOWN_OPERATION: RecoveryAction.ABORT,
            ErrorType.PRECONDITION_FAILED: RecoveryAction.ABORT,
            ErrorType.TIP_NOT_AVAILABLE: RecoveryAction.ABORT,
            ErrorType.MOTION_ERROR: RecoveryAction.ABORT,
        }

    def submit(self, job: IRJob) -> str:
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
        # Record the job status as pending
        self.job_status[job.job_id] = "pending"
        return job.job_id

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
        # Mark job as running
        self.job_status[job.job_id] = "running"
        # Compile
        worklist_lines = compile_ir(job)
        # Simulate execution
        sim_state = simulate_ir(job)
        # Mark job as completed
        self.job_status[job.job_id] = "completed"
        return worklist_lines, sim_state

    # ------------------------------------------------------------------
    # Job status and control methods
    # ------------------------------------------------------------------
    def status(self, job_id: str) -> Optional[str]:
        """Return the current status of the specified job.

        Args:
            job_id: The job identifier.

        Returns:
            The status string or ``None`` if unknown.
        """
        return self.job_status.get(job_id)

    def pause(self, job_id: str) -> None:
        """Pause a running job.

        Transitions the status from ``running`` to ``paused``.  In a
        real implementation this would send a pause command to the robot.
        """
        if self.job_status.get(job_id) == "running":
            self.job_status[job_id] = "paused"

    def resume(self, job_id: str) -> None:
        """Resume a paused job.

        Transitions the status from ``paused`` to ``running``.
        """
        if self.job_status.get(job_id) == "paused":
            self.job_status[job_id] = "running"

    def abort(self, job_id: str) -> None:
        """Abort a job.

        Sets the status to ``aborted`` and removes it from the queue if
        pending.  Does not stop execution of a job currently running in
        ``run_next`` because this prototype executes synchronously.
        """
        # Remove from queue if still pending
        for idx, job in enumerate(self.queue):
            if job.job_id == job_id:
                del self.queue[idx]
                break
        self.job_status[job_id] = "aborted"

    @property
    def state(self) -> Dict[str, Any]:
        """Return a snapshot of the job manager's state.

        Includes the deck state, the number of queued jobs and the
        current status of all known jobs.  Extend this method to include
        additional robot sensor and state information.
        """
        return {
            "deck_state": self.deck_state,
            "queued_jobs": len(self.queue),
            "job_status": dict(self.job_status),
        }