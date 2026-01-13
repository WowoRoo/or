"""Region value object."""

from dataclasses import dataclass
from typing import Set, Tuple
from domain.value_objects.point import Point


@dataclass(frozen=True)
class Region:
    """A connected region of points."""
    cells: Set[Point]
    
    def contains(self, point: Point) -> bool:
        """Check if point is in region."""
        return point in self.cells
    
    def get_bounds(self) -> Tuple[int, int, int, int]:
        """Get bounding box (min_x, min_y, max_x, max_y)."""
        if not self.cells:
            return (0, 0, 0, 0)
        
        xs = [p.x for p in self.cells]
        ys = [p.y for p in self.cells]
        return (min(xs), min(ys), max(xs), max(ys))
    
    def get_size(self) -> int:
        """Get number of cells in region."""
        return len(self.cells)

