"""Unit tests for the compiler module."""

import unittest

from fluent_robot.ir import IRJob, IRStep
from fluent_robot.compiler import compile_ir, well_to_position


class TestCompiler(unittest.TestCase):
    def test_well_to_position(self):
        # A1 -> 1, A2 -> 9, H12 -> 96
        self.assertEqual(well_to_position("A1"), 1)
        self.assertEqual(well_to_position("A2"), 9)
        self.assertEqual(well_to_position("H12"), 96)

    def test_compile_transfer(self):
        job = IRJob(
            version="1.0",
            job_id="test",
            steps=[IRStep(id="s1", op="transfer", args={
                "source_labware": "S1",
                "source_well": "A1",
                "dest_labware": "D1",
                "dest_well": "B1",
                "volume_uL": 10.0
            })]
        )
        lines = compile_ir(job)
        # Expect two lines: A and D
        self.assertEqual(len(lines), 2)
        self.assertTrue(lines[0].startswith("A;S1"))
        self.assertTrue(lines[1].startswith("D;D1"))
        # Volume formatted with two decimals
        self.assertIn("10.00", lines[0])
        self.assertIn("10.00", lines[1])
        # Numeric positions: A1 -> 1, B1 -> row B col1 -> position 2
        self.assertIn(";1;;", lines[0])
        self.assertIn(";2;;", lines[1])

    def test_compile_wash_decontaminate(self):
        job = IRJob(
            version="1.0",
            job_id="test2",
            steps=[
                IRStep(id="s1", op="wash", args={"scheme": 3}),
                IRStep(id="s2", op="decontaminate", args={})
            ]
        )
        lines = compile_ir(job)
        self.assertEqual(lines, ["W3;", "WD;"])


if __name__ == "__main__":
    unittest.main()