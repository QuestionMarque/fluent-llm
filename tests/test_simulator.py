"""Unit tests for the simulator module."""

import unittest

from fluent_llm.ir import IRJob, IRStep
from fluent_llm.simulator import simulate_ir


class TestSimulator(unittest.TestCase):
    def test_simulate_transfer_updates_volumes(self):
        job = IRJob(
            version="1.0",
            job_id="job1",
            steps=[IRStep(id="s1", op="transfer", args={
                "source_labware": "S1",
                "source_well": "A1",
                "dest_labware": "D1",
                "dest_well": "B1",
                "volume_uL": 25.0
            })]
        )
        state = simulate_ir(job)
        # A1 is position 1, B1 is position 2
        self.assertAlmostEqual(state["S1"][0], -25.0)
        self.assertAlmostEqual(state["D1"][1], 25.0)


if __name__ == "__main__":
    unittest.main()