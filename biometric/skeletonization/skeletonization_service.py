"""Skeletonization service."""

from domain.value_objects.workspace_bitmap import WorkspaceBitmap
from domain.value_objects.skeleton_result import SkeletonResult
from domain.enums.skeletonization_algorithm import SkeletonizationAlgorithm
from biometric.skeletonization.zhang_suen import zhang_suen
from biometric.skeletonization.hildritch import hildritch


class SkeletonizationService:
    """Service for skeletonization."""
    
    def skeletonize(
        self,
        bitmap: WorkspaceBitmap,
        algorithm: SkeletonizationAlgorithm
    ) -> SkeletonResult:
        """Skeletonize bitmap using specified algorithm."""
        if algorithm == SkeletonizationAlgorithm.ZHANG_SUEN:
            skeleton = zhang_suen(bitmap)
        elif algorithm == SkeletonizationAlgorithm.HILDRITCH:
            skeleton = hildritch(bitmap)
        else:
            raise ValueError(f"Unknown algorithm: {algorithm}")
        
        return SkeletonResult(
            skeleton_bitmap=skeleton,
            algorithm_used=algorithm.value
        )

