"""Unit tests for the capabilities loader.

These tests verify that the YAML registry in ``capabilities.yaml`` can be
loaded into Python and that the resulting structure contains the
expected top‑level keys.  If the file is missing or invalid, the
loader should return an empty dictionary.
"""

import unittest

from fluent_robot.capabilities import get_capabilities


class TestCapabilities(unittest.TestCase):
    def test_load_capabilities(self):
        data = get_capabilities()
        # The registry should be a dict with 'capabilities' and 'constraints'
        self.assertIsInstance(data, dict)
        # If the YAML file is present, both keys should be present
        # Since a placeholder file is provided, we check for them.
        self.assertIn("capabilities", data)
        self.assertIn("constraints", data)
        # The 'aspirate' operation should exist in the registry
        self.assertIn("aspirate", data["capabilities"])
        # The registry should define volume constraints
        volume_constraints = data["constraints"].get("volume")
        self.assertIsNotNone(volume_constraints)
        self.assertIn("min", volume_constraints)
        self.assertIn("max", volume_constraints)

    def test_no_yaml_returns_empty(self):
        # Temporarily rename the YAML file to simulate it missing
        import os
        import importlib
        path = os.path.join(os.path.dirname(__file__), "..", "fluent_robot", "capabilities.yaml")
        backup_path = path + ".bak"
        os.rename(path, backup_path)
        try:
            importlib.invalidate_caches()
            # Reload the module to force re-read of missing file
            from fluent_robot import capabilities  # type: ignore
            import importlib as _importlib
            _importlib.reload(capabilities)
            # Without the YAML, get_capabilities should return {}
            data = capabilities.get_capabilities()
            self.assertEqual(data, {})
        finally:
            # Restore the YAML file
            os.rename(backup_path, path)


if __name__ == "__main__":
    unittest.main()