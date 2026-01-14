"""Unit tests for the policy module.

These tests ensure that the risk classification functions return
expected values for known operations and default to 'block' for
unknown operations.
"""

import unittest

from fluent_llm.ir import IRStep
from fluent_llm.policy import classify_step, is_allowed


class TestPolicy(unittest.TestCase):
    def test_classify_known_operations(self):
        transfer = IRStep(id="s1", op="transfer", args={})
        wash = IRStep(id="s2", op="wash", args={})
        decon = IRStep(id="s3", op="decontaminate", args={})
        self.assertEqual(classify_step(transfer), "allow")
        self.assertEqual(classify_step(wash), "allow")
        self.assertEqual(classify_step(decon), "confirm")
        self.assertTrue(is_allowed(transfer))
        self.assertFalse(is_allowed(decon))

    def test_classify_unknown_operation(self):
        unknown = IRStep(id="s4", op="mix", args={})
        self.assertEqual(classify_step(unknown), "block")
        self.assertFalse(is_allowed(unknown))


if __name__ == "__main__":
    unittest.main()