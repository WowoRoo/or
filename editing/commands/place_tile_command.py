"""Command for placing a tile."""

from typing import Optional
from domain.value_objects.point import Point
from domain.entities.tile import Tile
from domain.entities.workspace import Workspace
from domain.enums.tile_type import TileType
from editing.commands.command import Command


class PlaceTileCommand(Command):
    """Command for placing a tile at a position."""
    
    def __init__(
        self,
        workspace: Workspace,
        point: Point,
        tile_type: TileType,
        rotation: float = 0.0
    ):
        self.workspace = workspace
        self.point = point
        self.tile_type = tile_type
        self.rotation = rotation
        self.previous_object = None  # Store full object reference
        self.tile_id: Optional[str] = None
    
    def execute(self) -> None:
        """Place tile at point."""
        active_layer = self.workspace.get_active_layer()
        if not active_layer:
            return
        
        # Save previous state (full object reference)
        cell = self.workspace.tilemap.get_cell(self.point.x, self.point.y)
        if cell and cell.map_object:
            self.previous_object = cell.map_object
            active_layer.remove_map_object(cell.map_object.id)
        
        # Create and place tile
        tile = Tile(self.tile_type, self.point, active_layer.id, self.rotation)
        self.tile_id = tile.id
        active_layer.add_map_object(tile)
        self.workspace.tilemap.set_cell(self.point.x, self.point.y, tile)
    
    def undo(self) -> None:
        """Remove placed tile and restore previous object if any."""
        active_layer = self.workspace.get_active_layer()
        if not active_layer:
            return
        
        # Remove placed tile
        if self.tile_id:
            active_layer.remove_map_object(self.tile_id)
            cell = self.workspace.tilemap.get_cell(self.point.x, self.point.y)
            if cell:
                cell.map_object = None
        
        # Restore previous object if any
        if self.previous_object:
            active_layer.add_map_object(self.previous_object)
            self.workspace.tilemap.set_cell(self.point.x, self.point.y, self.previous_object)

