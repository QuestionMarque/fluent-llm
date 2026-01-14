"""Unit tests for the llm_stub module."""

import unittest

from fluent_llm.llm_stub import plan_from_text


class TestLLMStub(unittest.TestCase):
    def test_plan_parses_transfer_and_wash(self):
        description = "Transfer 60 uL from plate P1 A2 to plate Q1 C3 and wash."
        job = plan_from_text(description)
        self.assertEqual(len(job.steps), 2)
        self.assertEqual(job.steps[0].op, "transfer")
        self.assertEqual(job.steps[1].op, "wash")
        # check args
        transfer = job.steps[0]
        self.assertEqual(transfer.args["source_labware"], "P1")
        self.assertEqual(transfer.args["source_well"], "A2")
        self.assertEqual(transfer.args["dest_labware"], "Q1")
        self.assertEqual(transfer.args["dest_well"], "C3")
        self.assertEqual(transfer.args["volume_uL"], 60.0)


if __name__ == "__main__":
    unittest.main()