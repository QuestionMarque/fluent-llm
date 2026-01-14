"""Unit tests for the preflight validator."""

import unittest

from fluent_robot.ir import IRJob, IRStep
from fluent_robot.preflight import preflight_check
from fluent_robot.state import ErrorType


class TestPreflight(unittest.TestCase):
    def setUp(self):
        # Basic deck_state with S1 and D1 present
        self.deck_state = {"S1": {}, "D1": {}}

    def test_preflight_valid(self):
        job = IRJob(
            version="1.0",
            job_id="job1",
            steps=[IRStep(id="s1", op="transfer", args={
                "source_labware": "S1",
                "source_well": "A1",
                "dest_labware": "D1",
                "dest_well": "B1",
                "volume_uL": 100.0
            })]
        )
        errors = preflight_check(job, self.deck_state)
        self.assertEqual(errors, [])

    def test_preflight_missing_labware(self):
        job = IRJob(
            version="1.0",
            job_id="job2",
            steps=[IRStep(id="s1", op="transfer", args={
                "source_labware": "S2",
                "source_well": "A1",
                "dest_labware": "D1",
                "dest_well": "B1",
                "volume_uL": 10.0
            })]
        )
        errors = preflight_check(job, self.deck_state)
        # Should have one labware_not_found error
        self.assertTrue(any(err[1] == ErrorType.LABWARE_NOT_FOUND for err in errors))

    def test_preflight_volume_out_of_range(self):
        job = IRJob(
            version="1.0",
            job_id="job3",
            steps=[IRStep(id="s1", op="transfer", args={
                "source_labware": "S1",
                "source_well": "A1",
                "dest_labware": "D1",
                "dest_well": "B1",
                "volume_uL": 2000.0  # Exceeds default max_volume_uL=1000
            })]
        )
        errors = preflight_check(job, self.deck_state)
        self.assertTrue(any(err[1] == ErrorType.VOLUME_OUT_OF_RANGE for err in errors))


if __name__ == "__main__":
    unittest.main()