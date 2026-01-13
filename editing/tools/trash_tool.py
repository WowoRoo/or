"""Trash tool for placing functional tiles."""

from domain.value_objects.point import Point
from domain.entities.workspace import Workspace
from domain.enums.functional_tile_type import FunctionalTileType
from domain.enums.tool_type import ToolType
from editing.tools.base_tool import BaseTool
from core.events.event_bus import EventBus


class TrashTool(BaseTool):
    """Tool for placing functional tiles."""
    
    def __init__(
        self,
        workspace: Workspace,
        event_bus: EventBus,
        functional_tile_type: FunctionalTileType = FunctionalTileType.PLAYER_START
    ):
        super().__init__(ToolType.TRASH)
        self.workspace = workspace
        self.event_bus = event_bus
        self.functional_tile_type = functional_tile_type
    
    def on_click(self, point: Point) -> None:
        """Place functional tile at point."""
        active_layer = self.workspace.get_active_layer()
        if not active_layer:
            return
        
        # Remove existing object
        cell = self.workspace.tilemap.get_cell(point.x, point.y)
        if cell and cell.map_object:
            active_layer.remove_map_object(cell.map_object.id)
        
        # Create and place functional tile
        from domain.entities.functional_tile import FunctionalTile
        func_tile = FunctionalTile(self.functional_tile_type, point, active_layer.id)
        active_layer.add_map_object(func_tile)
        self.workspace.tilemap.set_cell(point.x, point.y, func_tile)
    
    def on_drag(self, start: Point, end: Point) -> None:
        """Place functional tile at end point."""
        self.on_click(end)

