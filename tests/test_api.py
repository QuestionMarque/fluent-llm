"""Unit tests for the RobotAPI façade.

These tests verify that the API forwards operations to the job manager
correctly and exposes state and capabilities.  Because the API is a
thin wrapper, the tests focus on return values and state changes.
"""

import unittest

from fluent_llm.ir import IRJob, IRStep
from fluent_llm.job_manager import JobManager
from fluent_llm.api import RobotAPI


class TestRobotAPI(unittest.TestCase):
    def setUp(self) -> None:
        # Create a simple deck state with two labware items
        self.deck_state = {"S1": {}, "D1": {}}
        self.job_manager = JobManager(deck_state=self.deck_state)
        self.api = RobotAPI(self.job_manager)

    def _build_transfer_job(self) -> IRJob:
        return IRJob(
            version="1.0",
            job_id="job-test",
            name="Test transfer",
            steps=[IRStep(id="s1", op="transfer", args={
                "source_labware": "S1",
                "source_well": "A1",
                "dest_labware": "D1",
                "dest_well": "B1",
                "volume_uL": 20.0,
            }, preconditions=["robot.homed == true", "tip.attached == true"])],
            constraints={"require_homed": True},
        )

    def test_submit_and_get_status(self):
        job = self._build_transfer_job()
        job_id = self.api.submit_job(job)
        # API should return the job_id and job_manager should record status
        self.assertEqual(job_id, job.job_id)
        self.assertEqual(self.api.get_job_status(job_id), "pending")
        # Run the job through the manager
        self.job_manager.run_next()
        # Status should be completed after run
        self.assertEqual(self.api.get_job_status(job_id), "completed")

    def test_robot_state_and_capabilities(self):
        # The state should reflect deck_state and queued jobs
        state = self.api.get_robot_state()
        self.assertEqual(state["deck_state"], self.deck_state)
        # No jobs queued initially
        self.assertEqual(state["queued_jobs"], 0)
        # Capabilities registry should contain 'capabilities'
        caps = self.api.list_capabilities()
        self.assertIn("capabilities", caps)


if __name__ == "__main__":
    unittest.main()