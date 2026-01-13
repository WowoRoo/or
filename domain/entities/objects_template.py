"""Objects template entity."""

from uuid import UUID, uuid4
from domain.value_objects.point import Point
from domain.value_objects.template_layout import TemplateLayout
from domain.entities.tilemap import Tilemap


class ObjectsTemplate:
    """Predefined configuration of multiple tiles."""
    
    def __init__(
        self,
        name: str,
        layout: TemplateLayout,
        origin_point: Point
    ):
        self.id: UUID = uuid4()
        self.name: str = name
        self.layout: TemplateLayout = layout
        self.origin_point: Point = origin_point
    
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

