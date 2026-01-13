"""Features vector value object."""

from dataclasses import dataclass
from typing import Dict
import numpy as np
from domain.enums.feature_type import FeatureType


@dataclass(frozen=True)
class FeaturesVector:
    """Numerical representation of features."""
    vector: np.ndarray  # 1D array of features
    feature_counts: Dict[FeatureType, int]
    total_features: int
    
    def to_array(self) -> np.ndarray:
        """Get vector as numpy array."""
        return self.vector
    
    def distance_to(self, other: 'FeaturesVector') -> float:
        """Calculate Euclidean distance to another vector."""
        return float(np.linalg.norm(self.vector - other.vector))

