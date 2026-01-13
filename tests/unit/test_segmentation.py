"""Tests for segmentation (zaborization)."""

import pytest
import numpy as np
from domain.value_objects.workspace_bitmap import WorkspaceBitmap
from biometric.segmentation.segmentation_service import SegmentationService


def test_segmentation_finds_regions():
    """Test that segmentation finds regions."""
    # Create bitmap with foreground and background
    data = np.ones((10, 10), dtype=bool)  # Start with all True (background)
    data[3:7, 3:7] = False  # Foreground (0) in the middle
    # Rest is background (1)
    
    bitmap = WorkspaceBitmap(data, 10, 10)
    
    service = SegmentationService()
    result = service.segment(bitmap)
    
    assert result is not None
    assert len(result.foreground_regions) > 0
    assert len(result.background_regions) > 0

