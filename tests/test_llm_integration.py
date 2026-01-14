"""Unit tests for the llm_integration module.

These tests verify that generating IR from text returns an IR job and
that the repair loop raises errors when validation fails.
"""

import unittest

from fluent_llm.llm_integration import generate_ir_from_text


class TestLLMIntegration(unittest.TestCase):
    def test_generate_ir_valid(self):
        description = "Transfer 50 uL from plate S1 A1 to plate D1 B1"
        # Provide deck state so that preflight passes
        deck_state = {"S1": {}, "D1": {}}
        job = generate_ir_from_text(description, deck_state=deck_state)
        # Should return an IRJob with one transfer step
        self.assertEqual(len(job.steps), 1)
        self.assertEqual(job.steps[0].op, "transfer")

    def test_generate_ir_invalid(self):
        description = "Transfer 50 uL from plate X1 A1 to plate Y1 B1"
        deck_state = {"S1": {}, "D1": {}}
        # Expect a ValueError because labware is missing
        with self.assertRaises(ValueError):
            generate_ir_from_text(description, deck_state=deck_state)


if __name__ == "__main__":
    unittest.main()