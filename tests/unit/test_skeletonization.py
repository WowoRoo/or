"""Tests for skeletonization algorithms."""

import pytest
import numpy as np
from domain.value_objects.workspace_bitmap import WorkspaceBitmap
from domain.enums.skeletonization_algorithm import SkeletonizationAlgorithm
from biometric.skeletonization.skeletonization_service import SkeletonizationService
from biometric.skeletonization.zhang_suen import zhang_suen
from biometric.skeletonization.hildritch import hildritch


def test_zhang_suen_skeletonization():
    """Test Zhang-Suen algorithm on simple shape."""
    # Create simple line bitmap
    data = np.zeros((10, 10), dtype=bool)
    data[5, 2:8] = True  # Horizontal line
    
    bitmap = WorkspaceBitmap(data, 10, 10)
    result = zhang_suen(bitmap)
    
    assert result is not None
    assert result.width == 10
    assert result.height == 10
    # Skeleton should still have some pixels
    assert np.any(result.data)


def test_hildritch_skeletonization():
    """Test Hildritch algorithm on simple shape."""
    # Create simple line bitmap
    data = np.zeros((10, 10), dtype=bool)
    data[5, 2:8] = True  # Horizontal line
    
    bitmap = WorkspaceBitmap(data, 10, 10)
    result = hildritch(bitmap)
    
    assert result is not None
    assert result.width == 10
    assert result.height == 10
    # Skeleton should still have some pixels
    assert np.any(result.data)


def test_skeletonization_service():
    """Test skeletonization service."""
    service = SkeletonizationService()
    
    # Create test bitmap
    data = np.zeros((10, 10), dtype=bool)
    data[5, 2:8] = True
    
    bitmap = WorkspaceBitmap(data, 10, 10)
    
    # Test Zhang-Suen
    result = service.skeletonize(bitmap, SkeletonizationAlgorithm.ZHANG_SUEN)
    assert result.algorithm_used == "zhang_suen"
    assert result.skeleton_bitmap is not None
    
    # Test Hildritch
    result = service.skeletonize(bitmap, SkeletonizationAlgorithm.HILDRITCH)
    assert result.algorithm_used == "hildritch"
    assert result.skeleton_bitmap is not None

