"""Feature value object."""

from dataclasses import dataclass
from domain.value_objects.point import Point
from domain.enums.feature_type import FeatureType


@dataclass(frozen=True)
class Feature:
    """Detected biometric feature."""
    position: Point
    feature_type: FeatureType
    confidence: float  # 0.0-1.0
    
    def __eq__(self, other) -> bool:
        """Check equality."""
        if not isinstance(other, Feature):
            return False
        return (self.position == other.position and 
                self.feature_type == other.feature_type)

