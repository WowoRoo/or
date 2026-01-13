"""Main biometric processor."""

from domain.entities.workspace import Workspace
from domain.value_objects.preprocessing_parameters import PreprocessingParameters
from domain.value_objects.workspace_bitmap import WorkspaceBitmap
from domain.enums.skeletonization_algorithm import SkeletonizationAlgorithm
from biometric.preprocessing.preprocessing_service import PreprocessingService
from biometric.segmentation.segmentation_service import SegmentationService
from biometric.skeletonization.skeletonization_service import SkeletonizationService
from biometric.crossinizer.crossinizer_service import CrossinizerService
from biometric.features.feature_detector import FeatureDetector
from biometric.vectorization.vector_generator import VectorGenerator
from biometric.conversion.bitmap_converter import BitmapConverter


class BiometricProcessor:
    """Main processor for biometric algorithms."""
    
    def __init__(self):
        self.preprocessing_service = PreprocessingService()
        self.segmentation_service = SegmentationService()
        self.skeletonization_service = SkeletonizationService()
        self.crossinizer_service = CrossinizerService()
        self.feature_detector = FeatureDetector()
        self.vector_generator = VectorGenerator()
        self.bitmap_converter = BitmapConverter()
    
    def process_workspace(
        self,
        workspace: Workspace,
        preprocessing_params: PreprocessingParameters,
        skeleton_algorithm: SkeletonizationAlgorithm
    ) -> None:
        """Process workspace through biometric pipeline."""
        # Convert to bitmap
        bitmap = self.bitmap_converter.convert_to_bitmap(workspace)
        workspace.workspace_bitmap = bitmap
        
        # Preprocessing
        processed_bitmap = self.preprocessing_service.preprocess(bitmap, preprocessing_params)
        
        # Skeletonization
        skeleton_result = self.skeletonization_service.skeletonize(
            processed_bitmap,
            skeleton_algorithm
        )
        
        # Crossinizer
        crossinizer_result = self.crossinizer_service.analyze(skeleton_result)
        
        # Feature detection
        features = self.feature_detector.detect_features(crossinizer_result, skeleton_result)
        
        # Generate features vector
        features_vector = self.vector_generator.generate(features, workspace)
        
        # Store results in workspace
        workspace.features_vector = features_vector

