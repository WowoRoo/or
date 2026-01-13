"""Template converter service."""

from domain.entities.objects_template import ObjectsTemplate
from domain.value_objects.workspace_bitmap import WorkspaceBitmap
from domain.value_objects.template_layout import TemplateLayout
from domain.value_objects.point import Point
from domain.enums.tile_type import TileType
from biometric.segmentation.segmentation_service import SegmentationService


class TemplateConverter:
    """Service for converting images to templates."""
    
    def __init__(self, segmentation_service: SegmentationService):
        self.segmentation_service = segmentation_service
    
    def convert_bitmap_to_template(
        self,
        bitmap: WorkspaceBitmap,
        name: str
    ) -> ObjectsTemplate:
        """Convert bitmap to objects template using zaborization."""
        # Segment bitmap
        result = self.segmentation_service.segment(bitmap)
        
        # Create template from foreground regions
        tiles = []
        for region in result.foreground_regions:
            for point in region.cells:
                # Use GRASS as default tile type
                tiles.append((point, TileType.GRASS))
        
        layout = TemplateLayout(tiles=tiles, functional_tiles=[])
        origin = Point(0, 0)  # Default origin
        
        return ObjectsTemplate(name=name, layout=layout, origin_point=origin)

