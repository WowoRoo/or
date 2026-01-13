"""Tests for crossinizer."""

import pytest
import numpy as np
from domain.value_objects.workspace_bitmap import WorkspaceBitmap
from domain.value_objects.skeleton_result import SkeletonResult
from domain.enums.skeletonization_algorithm import SkeletonizationAlgorithm
from biometric.crossinizer.crossinizer_service import CrossinizerService


def test_crossinizer_detects_endpoints():
    """Test that crossinizer detects endpoints."""
    # Create simple line skeleton
    data = np.zeros((10, 10), dtype=bool)
    data[5, 3:7] = True  # Horizontal line
    
    skeleton_bitmap = WorkspaceBitmap(data, 10, 10)
    skeleton = SkeletonResult(skeleton_bitmap, "test")
    
    service = CrossinizerService()
    result = service.analyze(skeleton)
    
    # Should detect at least 2 endpoints (line ends)
    assert len(result.endpoints) >= 2


def test_crossinizer_detects_bifurcations():
    """Test that crossinizer detects bifurcations."""
    # Create Y-shape skeleton
    data = np.zeros((10, 10), dtype=bool)
    data[5, 5] = True  # Center
    data[4, 5] = True  # Up
    data[6, 4] = True  # Down-left
    data[6, 6] = True  # Down-right
    
    skeleton_bitmap = WorkspaceBitmap(data, 10, 10)
    skeleton = SkeletonResult(skeleton_bitmap, "test")
    
    service = CrossinizerService()
    result = service.analyze(skeleton)
    
    # Should detect at least 1 bifurcation
    assert len(result.bifurcations) >= 1

