"""Command for filling a region."""

from typing import List, Optional, Tuple
from domain.value_objects.point import Point
from domain.value_objects.region import Region
from domain.entities.tile import Tile
from domain.entities.workspace import Workspace
from domain.enums.tile_type import TileType
from editing.commands.command import Command


class FillRegionCommand(Command):
    """Command for filling a region with tiles."""
    
    def __init__(
        self,
        workspace: Workspace,
        region: Region,
        tile_type: TileType
    ):
        self.workspace = workspace
        self.region = region
        self.tile_type = tile_type
        self.placed_tiles: List[str] = []  # List of tile IDs
        self.previous_objects: List[Tuple[Point, object]] = []  # List of (point, object) tuples
    
    def execute(self) -> None:
        """Fill region with tiles."""
        active_layer = self.workspace.get_active_layer()
        if not active_layer:
            return
        
        # Save previous state and place new tiles
        for cell_point in self.region.cells:
            cell = self.workspace.tilemap.get_cell(cell_point.x, cell_point.y)
            if cell:
                # Save previous object
                if cell.map_object:
                    self.previous_objects.append((cell_point, cell.map_object))
                    active_layer.remove_map_object(cell.map_object.id)
                
                # Place new tile
                tile = Tile(self.tile_type, cell_point, active_layer.id)
                self.placed_tiles.append(tile.id)
                active_layer.add_map_object(tile)
                self.workspace.tilemap.set_cell(cell_point.x, cell_point.y, tile)
    
    def undo(self) -> None:
        """Remove placed tiles and restore previous objects."""
        active_layer = self.workspace.get_active_layer()
        if not active_layer:
            return
        
        # Remove placed tiles
        for tile_id in self.placed_tiles:
            active_layer.remove_map_object(tile_id)
        
        # Clear cells
        for cell_point in self.region.cells:
            cell = self.workspace.tilemap.get_cell(cell_point.x, cell_point.y)
            if cell:
                cell.map_object = None
        
        # Restore previous objects
        for point, obj in self.previous_objects:
            active_layer.add_map_object(obj)
            self.workspace.tilemap.set_cell(point.x, point.y, obj)

