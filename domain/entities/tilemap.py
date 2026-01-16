"""Tilemap entity."""

from typing import Dict, Optional, Tuple
from domain.value_objects.point import Point
from domain.value_objects.tile_cell import TileCell
from domain.value_objects.region import Region
from domain.entities.map_object import MapObject
from domain.value_objects.workspace_bitmap import WorkspaceBitmap
import numpy as np


class Tilemap:
    """Discrete 2D coordinate system for placing map objects."""
    
    def __init__(self, width: int, height: int):
        self.width: int = width
        self.height: int = height
        self.cells: Dict[Tuple[int, int], TileCell] = {}
        self._initialize_cells()
    
    def _initialize_cells(self) -> None:
        """Initialize all cells."""
        for y in range(self.height):
            for x in range(self.width):
                self.cells[(x, y)] = TileCell(Point(x, y))
    
    def get_cell(self, x: int, y: int) -> Optional[TileCell]:
        """Get cell at coordinates."""
        if not self.is_valid_coordinate(x, y):
            return None
        return self.cells.get((x, y))
    
    def set_cell(self, x: int, y: int, map_object: Optional[MapObject]) -> None:
        """Set map object in cell."""
        cell = self.get_cell(x, y)
        if cell:
            cell.map_object = map_object
    
    def get_region(self, x: int, y: int, fill_all: bool = False) -> Region:
        """Get region starting from point (for flood fill).
        
        Args:
            x: X coordinate
            y: Y coordinate
            fill_all: If True, fill all cells in connected region regardless of their state.
                     If False, fill only cells matching the starting cell's type (empty or same tile_type).
        """
        from domain.value_objects.region import Region
        from domain.value_objects.point import Point
        from domain.entities.tile import Tile
        from domain.enums.map_object_type import MapObjectType
        
        # Simple flood fill implementation
        if not self.is_valid_coordinate(x, y):
            return Region(set())
        
        start_cell = self.get_cell(x, y)
        if not start_cell:
            return Region(set())
        
        if fill_all:
            # Fill all cells in connected region, regardless of their state
            target_empty = None
            target_tile_type = None
            target_obj_type = None
        else:
            # Fill only cells matching the starting cell's type
            if start_cell.is_empty():
                target_empty = True
                target_tile_type = None
                target_obj_type = None
            else:
                target_empty = False
                # Check if it's a tile - match by tile_type
                if start_cell.map_object.get_type() == MapObjectType.TILE:
                    target_tile_type = start_cell.map_object.tile_type
                    target_obj_type = None
                else:
                    # For non-tile objects, match by exact object (original behavior)
                    target_tile_type = None
                    target_obj_type = start_cell.map_object.get_type()
        
        visited = set()
        stack = [Point(x, y)]
        region_cells = set()
        
        while stack:
            point = stack.pop()
            if point in visited:
                continue
            
            cell = self.get_cell(point.x, point.y)
            if not cell:
                continue
            
            if not fill_all:
                # Check if cell matches target state
                if target_empty is not None:
                    if target_empty:
                        if not cell.is_empty():
                            continue
                    else:
                        # Check if it's a tile and matches tile_type
                        if target_tile_type is not None:
                            if cell.is_empty():
                                continue
                            if cell.map_object.get_type() != MapObjectType.TILE:
                                continue
                            if cell.map_object.tile_type != target_tile_type:
                                continue
                        # Check if it's a non-tile object and matches type
                        elif target_obj_type is not None:
                            if cell.is_empty():
                                continue
                            if cell.map_object.get_type() != target_obj_type:
                                continue
            
            visited.add(point)
            region_cells.add(point)
            
            # Add neighbors (4-connectivity)
            for dx, dy in [(0, -1), (1, 0), (0, 1), (-1, 0)]:
                neighbor = Point(point.x + dx, point.y + dy)
                if neighbor not in visited and self.is_valid_coordinate(neighbor.x, neighbor.y):
                    stack.append(neighbor)
        
        return Region(region_cells)
    
    def is_valid_coordinate(self, x: int, y: int) -> bool:
        """Check if coordinates are valid."""
        return 0 <= x < self.width and 0 <= y < self.height
    
    def to_bitmap(self) -> WorkspaceBitmap:
        """Convert tilemap to binary bitmap."""
        # Initialize all pixels as BACKGROUND (True = 1)
        # Only tiles (FOREGROUND) will be set to False (0)
        bitmap = np.ones((self.height, self.width), dtype=bool)
        
        # Iterate through all coordinates, not just existing cells
        for y in range(self.height):
            for x in range(self.width):
                cell = self.get_cell(x, y)
                if cell and not cell.is_empty():
                    # Check if it's a tile (foreground)
                    from domain.enums.map_object_type import MapObjectType
                    if cell.map_object.get_type() == MapObjectType.TILE:
                        bitmap[y, x] = False  # FOREGROUND (tile)
                    # else: remains True (BACKGROUND) - functional tiles are background
        
        return WorkspaceBitmap(bitmap, self.width, self.height)

