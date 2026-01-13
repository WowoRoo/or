"""Bitmap converter service."""

from domain.entities.workspace import Workspace
from domain.value_objects.workspace_bitmap import WorkspaceBitmap


class BitmapConverter:
    """Service for converting workspace to bitmap."""
    
    def convert_to_bitmap(self, workspace: Workspace) -> WorkspaceBitmap:
        """Convert workspace to binary bitmap."""
        return workspace.tilemap.to_bitmap()

