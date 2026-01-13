"""Tests for preprocessing."""

import pytest
import numpy as np
from domain.value_objects.workspace_bitmap import WorkspaceBitmap
from domain.value_objects.preprocessing_parameters import PreprocessingParameters
from biometric.preprocessing.preprocessing_service import PreprocessingService


def test_preprocessing_binaryzation():
    """Test binaryzation."""
    # Create grayscale image
    data = np.array([[0.3, 0.7, 0.4], [0.6, 0.2, 0.8]], dtype=np.float32)
    bitmap = WorkspaceBitmap(data, 3, 2)
    
    params = PreprocessingParameters(
        noise_removal_enabled=False,
        filtering_enabled=False,
        binaryzation_threshold=0.5
    )
    
    service = PreprocessingService()
    result = service.preprocess(bitmap, params)
    
    assert result is not None
    assert result.width == 3
    assert result.height == 2
    assert result.data.dtype == bool


def test_preprocessing_noise_removal():
    """Test noise removal."""
    # Create bitmap with noise
    data = np.array([[True, False, True], [False, True, False]], dtype=bool)
    bitmap = WorkspaceBitmap(data, 3, 2)
    
    params = PreprocessingParameters(
        noise_removal_enabled=True,
        filtering_enabled=False,
        binaryzation_threshold=0.5
    )
    
    service = PreprocessingService()
    result = service.preprocess(bitmap, params)
    
    assert result is not None

