"""Utilities for enumerating robot capabilities and constraints.

This module loads a YAML file that describes the basic operations supported
by the robot (e.g. aspirate, dispense, wash) and any global constraints
(such as minimum/maximum volumes).  It serves as a placeholder for a
capability registry defined in phase 1 of the project plan.  The data
structure returned by :func:`get_capabilities` can be used by the
preflight validator and compiler to look up valid operations and their
parameters.  See ``capabilities.yaml`` for the initial schema.

If the YAML file cannot be parsed or is missing, ``get_capabilities``
returns an empty dictionary.  This allows callers to handle the absence
of a registry gracefully.  In a production system, failure to load
capabilities should be treated as a configuration error.
"""

from __future__ import annotations

import os
from typing import Any, Dict

try:
    import yaml  # type: ignore
except ImportError:  # pragma: no cover - PyYAML should be installed
    yaml = None  # type: ignore


_CAPABILITIES_FILE = os.path.join(os.path.dirname(__file__), "capabilities.yaml")


def get_capabilities() -> Dict[str, Any]:
    """Load the capabilities and constraints from the YAML registry.

    Returns:
        A dictionary containing the top‑level keys ``capabilities`` and
        ``constraints`` if available, otherwise an empty dictionary.

    The structure is defined by ``capabilities.yaml``.  Each entry under
    ``capabilities`` should specify a description and a list of
    parameters.  Constraints may define volume limits or other
    instrument‑wide settings.  Callers should guard against missing keys
    and provide sensible defaults.

    Example:

    >>> data = get_capabilities()
    >>> list(data["capabilities"].keys())
    ['aspirate', 'dispense', 'wash', 'decontaminate']
    """
    if yaml is None:
        # PyYAML is not installed; return empty registry
        return {}
    try:
        with open(_CAPABILITIES_FILE, "r", encoding="utf-8") as fh:
            data = yaml.safe_load(fh)
            if isinstance(data, dict):
                return data  # type: ignore[return-value]
    except FileNotFoundError:
        # capabilities.yaml is missing; return empty
        pass
    except Exception:
        # Parsing failed; return empty registry
        pass
    return {}
