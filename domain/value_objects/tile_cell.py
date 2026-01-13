"""Tile cell value object."""

from dataclasses import dataclass
from typing import Optional
from domain.value_objects.point import Point
from domain.entities.map_object import MapObject


@dataclass
class TileCell:
    """Single cell in tilemap."""
    position: Point
    map_object: Optional[MapObject] = None
    
    def is_empty(self) -> bool:
        """Check if cell is empty."""
        return self.map_object is None
    
    def clear(self) -> None:
        """Clear cell."""
        self.map_object = None

