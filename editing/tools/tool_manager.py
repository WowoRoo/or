"""Tool manager."""

from typing import Optional
from domain.enums.tool_type import ToolType
from editing.tools.base_tool import BaseTool
from editing.tools.brush_tool import BrushTool
from editing.tools.eraser_tool import EraserTool
from editing.tools.flood_tool import FloodTool
from editing.tools.trash_tool import TrashTool
from editing.commands.command_history import CommandHistory
from domain.entities.workspace import Workspace
from core.events.event_bus import EventBus
from biometric.segmentation.segmentation_service import SegmentationService


class ToolManager:
    """Manager for editing tools."""
    
    def __init__(
        self,
        workspace: Workspace,
        event_bus: EventBus,
        segmentation_service: SegmentationService,
        command_history: Optional[CommandHistory] = None
    ):
        self.workspace = workspace
        self.event_bus = event_bus
        self.segmentation_service = segmentation_service
        self.command_history = command_history
        self.active_tool: Optional[BaseTool] = None
        self._initialize_tools()
    
    def _initialize_tools(self) -> None:
        """Initialize all tools."""
        self.brush_tool = BrushTool(self.workspace, self.event_bus, self.command_history)
        self.eraser_tool = EraserTool(self.workspace, self.event_bus, self.command_history)
        self.flood_tool = FloodTool(self.workspace, self.event_bus, self.segmentation_service, self.command_history)
        self.trash_tool = TrashTool(self.workspace, self.event_bus)
    
    def set_active_tool(self, tool_type: ToolType) -> None:
        """Set active tool."""
        if tool_type == ToolType.BRUSH:
            self.active_tool = self.brush_tool
        elif tool_type == ToolType.ERASER:
            self.active_tool = self.eraser_tool
        elif tool_type == ToolType.FLOOD:
            self.active_tool = self.flood_tool
        elif tool_type == ToolType.TRASH:
            self.active_tool = self.trash_tool
        else:
            self.active_tool = None
        
        if self.active_tool:
            from core.events.domain_events import ToolActivated
            self.event_bus.publish(ToolActivated(tool_type))
    
    def get_active_tool(self) -> Optional[BaseTool]:
        """Get active tool."""
        return self.active_tool

