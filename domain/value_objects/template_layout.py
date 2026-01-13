"""Template layout value object."""

from dataclasses import dataclass
from typing import List, Tuple
from domain.value_objects.point import Point
from domain.enums.tile_type import TileType
from domain.enums.functional_tile_type import FunctionalTileType


@dataclass(frozen=True)
class TemplateLayout:
    """Layout of objects template."""
    tiles: List[Tuple[Point, TileType]]  # Relative positions
    functional_tiles: List[Tuple[Point, FunctionalTileType]]
    
    def get_bounds(self) -> Tuple[int, int, int, int]:
        """Get bounding box (min_x, min_y, max_x, max_y)."""
        all_points = [p for p, _ in self.tiles] + [p for p, _ in self.functional_tiles]
        if not all_points:
            return (0, 0, 0, 0)
        
        xs = [p.x for p in all_points]
        ys = [p.y for p in all_points]
        return (min(xs), min(ys), max(xs), max(ys))

