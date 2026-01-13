"""Skeleton result value object."""

from dataclasses import dataclass
from typing import List
from domain.value_objects.workspace_bitmap import WorkspaceBitmap
from domain.value_objects.point import Point


@dataclass(frozen=True)
class SkeletonResult:
    """Result of skeletonization algorithm."""
    skeleton_bitmap: WorkspaceBitmap
    algorithm_used: str
    
    def get_skeleton_points(self) -> List[Point]:
        """Get all skeleton points."""
        points = []
        for y in range(self.skeleton_bitmap.height):
            for x in range(self.skeleton_bitmap.width):
                if self.skeleton_bitmap.get_pixel(x, y):
                    points.append(Point(x, y))
        return points

