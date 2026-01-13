"""Functional tile entity."""

from domain.entities.map_object import MapObject
from domain.value_objects.point import Point
from domain.enums.map_object_type import MapObjectType
from domain.enums.functional_tile_type import FunctionalTileType


class FunctionalTile(MapObject):
    """Functional tile entity (enemies, checkpoints, etc.)."""
    
    def __init__(
        self,
        functional_tile_type: FunctionalTileType,
        position: Point,
        layer_id
    ):
        super().__init__(position, layer_id)
        self.functional_tile_type: FunctionalTileType = functional_tile_type
    
    def get_type(self) -> MapObjectType:
        """Get type of map object."""
        return MapObjectType.FUNCTIONAL_TILE

