"""Skeletonization algorithm enumeration."""

from enum import Enum


class SkeletonizationAlgorithm(Enum):
    """Algorithm for skeletonization."""
    ZHANG_SUEN = "zhang_suen"
    HILDRITCH = "hildritch"

