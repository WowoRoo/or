"""Command for removing an object."""

from typing import Optional
from domain.value_objects.point import Point
from domain.entities.workspace import Workspace
from editing.commands.command import Command


class RemoveObjectCommand(Command):
    """Command for removing an object at a position."""
    
    def __init__(self, workspace: Workspace, point: Point):
        self.workspace = workspace
        self.point = point
        self.removed_object_id: Optional[str] = None
        self.removed_object = None
        self.removed_object_type: Optional[str] = None
    
    def execute(self) -> None:
        """Remove object at point."""
        active_layer = self.workspace.get_active_layer()
        if not active_layer:
            return
        
        cell = self.workspace.tilemap.get_cell(self.point.x, self.point.y)
        if cell and cell.map_object:
            self.removed_object_id = cell.map_object.id
            self.removed_object = cell.map_object
            from domain.enums.map_object_type import MapObjectType
            if cell.map_object.get_type() == MapObjectType.TILE:
                self.removed_object_type = "tile"
            else:
                self.removed_object_type = "functional"
            
            active_layer.remove_map_object(cell.map_object.id)
            cell.map_object = None
    
    def undo(self) -> None:
        """Restore removed object."""
        active_layer = self.workspace.get_active_layer()
        if not active_layer or not self.removed_object:
            return
        
        # Restore object
        active_layer.add_map_object(self.removed_object)
        self.workspace.tilemap.set_cell(self.point.x, self.point.y, self.removed_object)

