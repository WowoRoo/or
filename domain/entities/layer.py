"""Layer entity."""

from uuid import UUID, uuid4
from typing import List
from domain.entities.map_object import MapObject
from domain.enums.layer_type import LayerType
from domain.value_objects.references import TileListReference, FunctionalTileListReference


class Layer:
    """Layer entity grouping map objects."""
    
    def __init__(
        self,
        name: str,
        layer_type: LayerType,
        tile_list_reference: TileListReference,
        functional_tile_list_reference: FunctionalTileListReference
    ):
        self.id: UUID = uuid4()
        self.name: str = name
        self.visible: bool = True
        self.editable: bool = True
        self.layer_type: LayerType = layer_type
        self.map_objects: List[MapObject] = []
        self.tile_list_reference: TileListReference = tile_list_reference
        self.functional_tile_list_reference: FunctionalTileListReference = functional_tile_list_reference
    
    def add_map_object(self, map_object: MapObject) -> None:
        """Add map object to layer."""
        self.map_objects.append(map_object)
    
    def remove_map_object(self, map_object_id: UUID) -> None:
        """Remove map object from layer."""
        self.map_objects = [obj for obj in self.map_objects if obj.id != map_object_id]
    
    def get_map_objects(self) -> List[MapObject]:
        """Get all map objects in layer."""
        return self.map_objects.copy()

