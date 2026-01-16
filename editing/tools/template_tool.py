"""Template tool for placing templates."""

from typing import Optional
from domain.value_objects.point import Point
from domain.entities.workspace import Workspace
from domain.entities.objects_template import ObjectsTemplate
from domain.enums.tool_type import ToolType
from editing.tools.base_tool import BaseTool
from editing.commands.command_history import CommandHistory
from editing.commands.place_template_command import PlaceTemplateCommand
from core.events.event_bus import EventBus


class TemplateTool(BaseTool):
    """Tool for placing templates."""
    
    def __init__(
        self,
        workspace: Workspace,
        event_bus: EventBus,
        command_history: Optional[CommandHistory] = None,
        template: Optional[ObjectsTemplate] = None,
        template_color: Optional[tuple] = None,
        scale: float = 1.0
    ):
        super().__init__(ToolType.TEMPLATE)
        self.workspace = workspace
        self.event_bus = event_bus
        self.command_history = command_history
        self.template = template
        self.template_color = template_color  # (r, g, b) for coloring tiles
        self.scale = scale  # Scale factor (0.1 to 1.0)
    
    def set_template(self, template: Optional[ObjectsTemplate]) -> None:
        """Set active template."""
        self.template = template
    
    def set_template_color(self, color: Optional[tuple]) -> None:
        """Set template color (r, g, b)."""
        self.template_color = color
    
    def set_scale(self, scale: float) -> None:
        """Set template scale (0.1 to 1.0)."""
        self.scale = max(0.1, min(1.0, scale))
    
    def on_click(self, point: Point) -> None:
        """Place template at point."""
        if not self.template:
            return
        
        if self.command_history:
            # Use command pattern for undo/redo
            command = PlaceTemplateCommand(self.workspace, self.template, point, self.template_color, self.scale)
            self.command_history.execute(command)
        else:
            # Fallback to direct execution
            command = PlaceTemplateCommand(self.workspace, self.template, point, self.template_color, self.scale)
            command.execute()
    
    def on_drag(self, start: Point, end: Point) -> None:
        """Handle drag from start to end."""
        # Template tool doesn't support drag
        pass

