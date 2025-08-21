"""Flaggle: Python feature flag management library.

This package provides the Flaggle class for managing feature flags, as well as the Flag, FlagType, and FlagOperation classes for defining and evaluating individual flags.

Exports:
    Flaggle: Main entry point for feature flag management.
    Flag: Represents a single feature flag.
    FlagType: Enum of supported flag value types.
    FlagOperation: Enum of supported flag operations.
"""

from python_flaggle.flaggle import Flaggle
from python_flaggle.flag import Flag, FlagOperation, FlagType

__all__ = ["FlagType", "FlagOperation", "Flag", "Flaggle"]
__version__ = "0.4.0a1"
__author__ = "Asaph Diniz"
__email__ = "contato@asaph.dev.br"
