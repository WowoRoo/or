"""Vector generator for features."""

import numpy as np
from typing import List
from domain.value_objects.feature import Feature
from domain.value_objects.features_vector import FeaturesVector
from domain.enums.feature_type import FeatureType
from domain.entities.workspace import Workspace


class VectorGenerator:
    """Service for generating features vector."""
    
    def generate(self, features: List[Feature], workspace: Workspace) -> FeaturesVector:
        """Generate features vector from features."""
        # Count features by type
        feature_counts = {
            FeatureType.ENDPOINT: 0,
            FeatureType.BIFURCATION: 0,
            FeatureType.CROSSING: 0
        }
        
        for feature in features:
            feature_counts[feature.feature_type] += 1
        
        # Calculate density
        area = workspace.metadata.width * workspace.metadata.height
        density = len(features) / area if area > 0 else 0.0
        
        # Create vector
        vector = np.array([
            float(feature_counts[FeatureType.ENDPOINT]),
            float(feature_counts[FeatureType.BIFURCATION]),
            float(feature_counts[FeatureType.CROSSING]),
            density
        ])
        
        return FeaturesVector(
            vector=vector,
            feature_counts=feature_counts,
            total_features=len(features)
        )

