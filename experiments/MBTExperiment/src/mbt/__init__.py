"""MBTExperiment — two venue facts, measured. No premium, no order, no position.

This package reads an initial margin and a bid-ask. It transmits nothing. The
no-transmit property is enforced by an AST walk over this package's parse tree
in :mod:`tools.no_transmit_scan`, not by prose and not by a text search.

Every pattern here is **copied** from solcopy, InsiderExperiment and
VRPExperiment rather than imported from them. An import would make a closed
repository a live dependency of an open one, and the next refactor here would
edit a sealed artifact.
"""

from __future__ import annotations

__all__ = ["__version__"]

__version__ = "0.1.0"
