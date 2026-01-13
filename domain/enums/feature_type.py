"""Feature type enumeration."""

from enum import Enum


class FeatureType(Enum):
    """Type of biometric feature."""
    ENDPOINT = "endpoint"
    BIFURCATION = "bifurcation"
    CROSSING = "crossing"

