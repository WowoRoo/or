"""Preprocessing service for image preparation."""

import numpy as np
from domain.value_objects.workspace_bitmap import WorkspaceBitmap
from domain.value_objects.preprocessing_parameters import PreprocessingParameters


class PreprocessingService:
    """Service for preprocessing images before biometric analysis."""
    
    def preprocess(
        self,
        bitmap: WorkspaceBitmap,
        parameters: PreprocessingParameters
    ) -> WorkspaceBitmap:
        """Preprocess bitmap."""
        # 1. Binaryzation
        binary = self._binaryze(bitmap, parameters.binaryzation_threshold)
        
        # 2. Usuwanie szumu (jeśli włączone)
        if parameters.noise_removal_enabled:
            binary = self._remove_noise(binary, parameters.noise_removal_threshold)
        
        # 3. Filtracja (jeśli włączona)
        if parameters.filtering_enabled:
            binary = self._apply_filter(binary, parameters.filter_type, parameters.filter_size)
        
        return WorkspaceBitmap(binary, bitmap.width, bitmap.height)
    
    def _binaryze(self, bitmap: WorkspaceBitmap, threshold: float) -> np.ndarray:
        """Convert to binary using threshold."""
        # Convert to float if needed
        if bitmap.data.dtype == bool:
            data = bitmap.data.astype(np.float32)
        else:
            data = bitmap.data.astype(np.float32) / 255.0
        
        # Apply threshold
        binary = (data >= threshold).astype(bool)
        return binary
    
    def _remove_noise(self, bitmap: np.ndarray, threshold: float) -> np.ndarray:
        """Remove noise using median filter."""
        return self._median_filter(bitmap, 3)
    
    def _median_filter(self, bitmap: np.ndarray, size: int) -> np.ndarray:
        """Apply median filter (own implementation)."""
        height, width = bitmap.shape
        result = bitmap.copy()
        half = size // 2
        
        for y in range(half, height - half):
            for x in range(half, width - half):
                # Get neighborhood
                neighborhood = []
                for dy in range(-half, half + 1):
                    for dx in range(-half, half + 1):
                        ny, nx = y + dy, x + dx
                        if 0 <= ny < height and 0 <= nx < width:
                            neighborhood.append(bitmap[ny, nx])
                
                # Get median
                neighborhood.sort()
                median_idx = len(neighborhood) // 2
                result[y, x] = neighborhood[median_idx]
        
        return result
    
    def _apply_filter(self, bitmap: np.ndarray, filter_type: str, size: int) -> np.ndarray:
        """Apply filter."""
        if filter_type == "median":
            return self._median_filter(bitmap, size)
        elif filter_type == "gaussian":
            return self._gaussian_blur(bitmap, size)
        else:
            return bitmap
    
    def _gaussian_blur(self, bitmap: np.ndarray, size: int) -> np.ndarray:
        """Apply Gaussian blur (simplified implementation)."""
        # Simple box blur approximation
        height, width = bitmap.shape
        result = bitmap.copy().astype(np.float32)
        half = size // 2
        
        # Horizontal pass
        temp = result.copy()
        for y in range(height):
            for x in range(half, width - half):
                sum_val = 0.0
                for dx in range(-half, half + 1):
                    sum_val += result[y, x + dx]
                temp[y, x] = sum_val / size
        
        # Vertical pass
        for y in range(half, height - half):
            for x in range(width):
                sum_val = 0.0
                for dy in range(-half, half + 1):
                    sum_val += temp[y + dy, x]
                result[y, x] = sum_val / size
        
        return result.astype(bool)

