"""Base map object entity."""

from abc import ABC, abstractmethod
from uuid import UUID, uuid4
from domain.value_objects.point import Point
from domain.enums.map_object_type import MapObjectType


class MapObject(ABC):
    """Base class for all map objects."""
    
    def __init__(self, position: Point, layer_id: UUID):
        self.id: UUID = uuid4()
        self.position: Point = position
        self.layer_id: UUID = layer_id
    
    @abstractmethod
    def get_type(self) -> MapObjectType:
        """Get type of map object."""
        pass

