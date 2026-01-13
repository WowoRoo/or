"""Tile entity."""

from typing import Optional
from domain.entities.map_object import MapObject
from domain.value_objects.point import Point
from domain.enums.map_object_type import MapObjectType
from domain.enums.tile_type import TileType


class Tile(MapObject):
    """Tile entity representing terrain."""
    
    def __init__(
        self,
        tile_type: TileType,
        position: Point,
        layer_id,
        rotation: float = 0.0,
        direction: Optional[object] = None  # Direction from CROSSINIZER
    ):
        super().__init__(position, layer_id)
        self.tile_type: TileType = tile_type
        self.rotation: float = rotation  # 0-360 degrees
        self.direction: Optional[object] = direction
    
    def get_type(self) -> MapObjectType:
        """Get type of map object."""
        return MapObjectType.TILE

