"""Workspace bitmap value object."""

from dataclasses import dataclass
import numpy as np
from PIL import Image
from domain.value_objects.point import Point


@dataclass(frozen=True)
class WorkspaceBitmap:
    """Binary bitmap representation of workspace."""
    data: np.ndarray  # dtype=bool or uint8, shape=(height, width)
    width: int
    height: int
    
    def get_pixel(self, x: int, y: int) -> bool:
        """Get pixel value at coordinates."""
        if not self.is_valid_coordinate(x, y):
            return False
        return bool(self.data[y, x])
    
    def set_pixel(self, x: int, y: int, value: bool) -> 'WorkspaceBitmap':
        """Create new bitmap with pixel set."""
        new_data = self.data.copy()
        if self.is_valid_coordinate(x, y):
            new_data[y, x] = value
        return WorkspaceBitmap(new_data, self.width, self.height)
    
    def is_valid_coordinate(self, x: int, y: int) -> bool:
        """Check if coordinates are valid."""
        return 0 <= x < self.width and 0 <= y < self.height
    
    def to_image(self) -> Image.Image:
        """Convert to PIL Image."""
        # Convert to uint8 for PIL
        img_data = (self.data.astype(np.uint8) * 255)
        return Image.fromarray(img_data, mode='L')

