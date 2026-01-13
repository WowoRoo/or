"""Crossinizer service for detecting features."""

from typing import List, Tuple
from domain.value_objects.skeleton_result import SkeletonResult
from domain.value_objects.crossinizer_result import CrossinizerResult
from domain.value_objects.point import Point


class CrossinizerService:
    """Service for analyzing skeleton and detecting features."""
    
    def analyze(self, skeleton: SkeletonResult) -> CrossinizerResult:
        """Analyze skeleton and detect endpoints, bifurcations, crossings."""
        endpoints = []
        bifurcations = []
        crossings = []
        connections = []
        
        bitmap = skeleton.skeleton_bitmap
        
        for y in range(bitmap.height):
            for x in range(bitmap.width):
                if bitmap.get_pixel(x, y):
                    neighbors = self._count_neighbors(bitmap, x, y)
                    point = Point(x, y)
                    
                    if neighbors == 1:
                        endpoints.append(point)
                    elif neighbors == 3:
                        bifurcations.append(point)
                    elif neighbors >= 4:
                        crossings.append(point)
                    # neighbors == 2 is regular point
        
        # Find connections between special points
        connections = self._find_connections(bitmap, endpoints, bifurcations, crossings)
        
        return CrossinizerResult(
            endpoints=endpoints,
            bifurcations=bifurcations,
            crossings=crossings,
            connections=connections
        )
    
    def _count_neighbors(self, bitmap, x: int, y: int) -> int:
        """Count neighbors in 8-connectivity."""
        count = 0
        for dy in [-1, 0, 1]:
            for dx in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                nx, ny = x + dx, y + dy
                if bitmap.is_valid_coordinate(nx, ny) and bitmap.get_pixel(nx, ny):
                    count += 1
        return count
    
    def _find_connections(
        self,
        bitmap,
        endpoints: List[Point],
        bifurcations: List[Point],
        crossings: List[Point]
    ) -> List[Tuple[Point, Point]]:
        """Find connections between special points."""
        connections = []
        all_special_points = set(endpoints + bifurcations + crossings)
        
        # For each special point, trace path to next special point
        for start_point in all_special_points:
            visited = set()
            self._trace_path(bitmap, start_point, all_special_points, visited, connections)
        
        return connections
    
    def _trace_path(
        self,
        bitmap,
        start: Point,
        special_points: set,
        visited: set,
        connections: List[Tuple[Point, Point]]
    ) -> None:
        """Trace path from start point to next special point."""
        if start in visited:
            return
        
        visited.add(start)
        stack = [(start, start)]  # (current, origin)
        
        while stack:
            current, origin = stack.pop()
            
            # Check neighbors
            for dy in [-1, 0, 1]:
                for dx in [-1, 0, 1]:
                    if dx == 0 and dy == 0:
                        continue
                    
                    neighbor = Point(current.x + dx, current.y + dy)
                    
                    if not bitmap.is_valid_coordinate(neighbor.x, neighbor.y):
                        continue
                    
                    if not bitmap.get_pixel(neighbor.x, neighbor.y):
                        continue
                    
                    if neighbor == origin:
                        continue
                    
                    # Found another special point
                    if neighbor in special_points:
                        connection = (start, neighbor)
                        reverse_connection = (neighbor, start)
                        if connection not in connections and reverse_connection not in connections:
                            connections.append(connection)
                        continue
                    
                    # Continue tracing
                    if neighbor not in visited:
                        visited.add(neighbor)
                        stack.append((neighbor, current))

