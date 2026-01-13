"""Image importer service."""

from PIL import Image
import numpy as np
from domain.value_objects.workspace_bitmap import WorkspaceBitmap


class ImageImporter:
    """Service for importing RGB images."""
    
    def import_image(self, filepath: str) -> WorkspaceBitmap:
        """Import image from file."""
        img = Image.open(filepath)
        
        # Convert to grayscale if needed
        if img.mode != 'L':
            img = img.convert('L')
        
        # Convert to numpy array
        img_array = np.array(img, dtype=np.float32) / 255.0
        
        # Convert to binary bitmap (threshold at 0.5)
        binary = (img_array >= 0.5).astype(bool)
        
        return WorkspaceBitmap(binary, img.width, img.height)

