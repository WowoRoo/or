"""Berlin wall value object."""

from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True)
class BerlinWall:
    """Boundary of workspace."""
    min_x: int
    min_y: int
    max_x: int
    max_y: int
    
    def contains(self, x: int, y: int) -> bool:
        """Check if point is within bounds."""
        return self.min_x <= x <= self.max_x and self.min_y <= y <= self.max_y
    
    def get_bounds(self) -> Tuple[int, int, int, int]:
        """Get bounds as tuple."""
        return (self.min_x, self.min_y, self.max_x, self.max_y)

