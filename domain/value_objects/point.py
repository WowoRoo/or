"""Point value object."""

from dataclasses import dataclass
import math


@dataclass(frozen=True)
class Point:
    """2D point with integer coordinates."""
    x: int
    y: int
    
    def distance_to(self, other: 'Point') -> float:
        """Calculate Euclidean distance to another point."""
        dx = self.x - other.x
        dy = self.y - other.y
        return math.sqrt(dx * dx + dy * dy)
    
    def __add__(self, other: 'Point') -> 'Point':
        """Add two points."""
        return Point(self.x + other.x, self.y + other.y)
    
    def __sub__(self, other: 'Point') -> 'Point':
        """Subtract two points."""
        return Point(self.x - other.x, self.y - other.y)

