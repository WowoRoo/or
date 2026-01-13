"""Flood tool for filling regions."""

from typing import Optional
from domain.value_objects.point import Point
from domain.entities.workspace import Workspace
from domain.enums.tile_type import TileType
from domain.enums.tool_type import ToolType
from editing.tools.base_tool import BaseTool
from editing.commands.command_history import CommandHistory
from editing.commands.fill_region_command import FillRegionCommand
from biometric.segmentation.segmentation_service import SegmentationService
from core.events.event_bus import EventBus
from core.events.domain_events import RegionFilled


class FloodTool(BaseTool):
    """Tool for filling regions using zaborization."""
    
    def __init__(
        self,
        workspace: Workspace,
        event_bus: EventBus,
        segmentation_service: SegmentationService,
        command_history: Optional[CommandHistory] = None,
        tile_type: TileType = TileType.GRASS
    ):
        super().__init__(ToolType.FLOOD)
        self.workspace = workspace
        self.event_bus = event_bus
        self.segmentation_service = segmentation_service
        self.command_history = command_history
        self.tile_type = tile_type
    
    def on_click(self, point: Point) -> None:
        """Fill region starting from point.
        
        Fills all connected cells that match the starting cell's type:
        - If starting cell is empty, fills all connected empty cells
        - If starting cell is a tile (e.g., grass), fills all connected tiles of the same type
        - If starting cell is a functional tile, fills all connected functional tiles of the same type
        """
        active_layer = self.workspace.get_active_layer()
        if not active_layer:
            return
        
        # Get region using flood fill - fill cells matching the starting cell's type
        region = self.workspace.tilemap.get_region(point.x, point.y, fill_all=False)
        
        if self.command_history:
            # Use command pattern for undo/redo
            command = FillRegionCommand(self.workspace, region, self.tile_type)
            self.command_history.execute(command)
        else:
            # Fallback to direct execution
            # Fill all cells in region
            for cell_point in region.cells:
                cell = self.workspace.tilemap.get_cell(cell_point.x, cell_point.y)
                if cell:
                    # Remove existing object
                    if cell.map_object:
                        active_layer.remove_map_object(cell.map_object.id)
                    
                    # Place new tile
                    from domain.entities.tile import Tile
                    tile = Tile(self.tile_type, cell_point, active_layer.id)
                    active_layer.add_map_object(tile)
                    self.workspace.tilemap.set_cell(cell_point.x, cell_point.y, tile)
        
        self.event_bus.publish(RegionFilled(len(region.cells)))
    
    def on_drag(self, start: Point, end: Point) -> None:
        """Flood fill at end point."""
        self.on_click(end)

