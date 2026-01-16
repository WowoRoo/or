"""Objects template entity."""

from uuid import UUID, uuid4
from typing import Optional
from domain.value_objects.point import Point
from domain.value_objects.template_layout import TemplateLayout
from domain.value_objects.workspace_bitmap import WorkspaceBitmap
from domain.entities.tilemap import Tilemap


class ObjectsTemplate:
    """Predefined configuration of multiple tiles."""
    
    def __init__(
        self,
        name: str,
        layout: TemplateLayout,
        origin_point: Point,
        source_bitmap: Optional[WorkspaceBitmap] = None
    ):
        self.id: UUID = uuid4()
        self.name: str = name
        self.layout: TemplateLayout = layout
        self.origin_point: Point = origin_point
        self.source_bitmap: Optional[WorkspaceBitmap] = source_bitmap  # Full bitmap for scaling
    
    def get_center(self) -> Point:
        """Get center point of template."""
        bounds = self.layout.get_bounds()
        if bounds == (0, 0, 0, 0):
            return Point(0, 0)
        min_x, min_y, max_x, max_y = bounds
        center_x = (min_x + max_x) // 2
        center_y = (min_y + max_y) // 2
        return Point(center_x, center_y)
    
    def apply_to_tilemap(self, tilemap: Tilemap, position: Point) -> None:
        """Apply template to tilemap at position."""
        offset = Point(position.x - self.origin_point.x, position.y - self.origin_point.y)
        
        # Apply tiles
        for rel_pos, tile_type in self.layout.tiles:
            abs_pos = rel_pos + offset
            if tilemap.is_valid_coordinate(abs_pos.x, abs_pos.y):
                from domain.entities.tile import Tile
                from domain.enums.layer_type import LayerType
                # Note: This is simplified - in full implementation would need layer_id
                # For now, we'll just mark the cell
                cell = tilemap.get_cell(abs_pos.x, abs_pos.y)
                if cell:
                    # Would need proper layer context to create tile
                    pass
        
        # Apply functional tiles similarly
        for rel_pos, func_tile_type in self.layout.functional_tiles:
            abs_pos = rel_pos + offset
            if tilemap.is_valid_coordinate(abs_pos.x, abs_pos.y):
                # Similar to tiles
                pass

