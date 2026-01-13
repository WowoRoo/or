"""Feature detector service."""

from typing import List
from domain.value_objects.crossinizer_result import CrossinizerResult
from domain.value_objects.skeleton_result import SkeletonResult
from domain.value_objects.feature import Feature
from domain.enums.feature_type import FeatureType


class FeatureDetector:
    """Service for detecting features from crossinizer results."""
    
    def detect_features(
        self,
        crossinizer_result: CrossinizerResult,
        skeleton: SkeletonResult
    ) -> List[Feature]:
        """Detect features from crossinizer results."""
        features = []
        
        # Convert endpoints
        for endpoint in crossinizer_result.endpoints:
            features.append(Feature(
                position=endpoint,
                feature_type=FeatureType.ENDPOINT,
                confidence=1.0
            ))
        
        # Convert bifurcations
        for bifurcation in crossinizer_result.bifurcations:
            features.append(Feature(
                position=bifurcation,
                feature_type=FeatureType.BIFURCATION,
                confidence=1.0
            ))
        
        # Convert crossings
        for crossing in crossinizer_result.crossings:
            features.append(Feature(
                position=crossing,
                feature_type=FeatureType.CROSSING,
                confidence=1.0
            ))
        
        return features

