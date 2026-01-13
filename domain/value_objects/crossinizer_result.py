"""Crossinizer result value object."""

from dataclasses import dataclass
from typing import List, Tuple, Optional
from domain.value_objects.point import Point
from domain.enums.feature_type import FeatureType


@dataclass(frozen=True)
class CrossinizerResult:
    """Result of crossinizer analysis."""
    endpoints: List[Point]
    bifurcations: List[Point]
    crossings: List[Point]
    connections: List[Tuple[Point, Point]]  # Connections between points
    
    def get_feature_at(self, point: Point) -> Optional[FeatureType]:
        """Get feature type at point."""
        if point in self.endpoints:
            return FeatureType.ENDPOINT
        if point in self.bifurcations:
            return FeatureType.BIFURCATION
        if point in self.crossings:
            return FeatureType.CROSSING
        return None

