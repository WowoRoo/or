"""Zaborization result value object."""

from dataclasses import dataclass
from typing import List
import numpy as np
from domain.value_objects.region import Region
from domain.value_objects.workspace_bitmap import WorkspaceBitmap


@dataclass(frozen=True)
class ZaborizationResult:
    """Result of segmentation (zaborization)."""
    foreground_regions: List[Region]
    background_regions: List[Region]
    segmentation_map: np.ndarray  # Map of region IDs
    
    def get_foreground_mask(self) -> WorkspaceBitmap:
        """Get foreground mask as bitmap for skeletonization.
        Returns bitmap where foreground pixels = True (1), background = False (0).
        For skeletonization, we want to skeletonize the True pixels.
        """
        # Create binary mask from foreground regions
        if len(self.foreground_regions) == 0:
            shape = self.segmentation_map.shape
            return WorkspaceBitmap(
                np.zeros(shape, dtype=bool),
                shape[1],
                shape[0]
            )
        
        # Use segmentation map to create mask - foreground regions have positive IDs
        mask = self.segmentation_map > 0
        return WorkspaceBitmap(
            mask.astype(bool),
            mask.shape[1],
            mask.shape[0]
        )
    
    def get_background_mask(self) -> WorkspaceBitmap:
        """Get background mask as bitmap for skeletonization.
        Returns bitmap where background pixels = True (1), foreground = False (0).
        For skeletonization, we want to skeletonize the True pixels.
        """
        # Background regions have negative IDs in segmentation map
        if len(self.background_regions) == 0:
            shape = self.segmentation_map.shape
            return WorkspaceBitmap(
                np.zeros(shape, dtype=bool),
                shape[1],
                shape[0]
            )
        
        # Use segmentation map - background regions have negative IDs
        mask = self.segmentation_map < 0
        return WorkspaceBitmap(
            mask.astype(bool),
            mask.shape[1],
            mask.shape[0]
        )

