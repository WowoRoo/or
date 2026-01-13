"""Eraser tool for removing objects."""

from typing import Optional
from domain.value_objects.point import Point
from domain.entities.workspace import Workspace
from domain.enums.tool_type import ToolType
from editing.tools.base_tool import BaseTool
from editing.commands.command_history import CommandHistory
from editing.commands.remove_object_command import RemoveObjectCommand
from core.events.event_bus import EventBus
from core.events.domain_events import MapObjectErased


class EraserTool(BaseTool):
    """Tool for erasing map objects."""
    
    def __init__(
        self,
        workspace: Workspace,
        event_bus: EventBus,
        command_history: Optional[CommandHistory] = None
    ):
        super().__init__(ToolType.ERASER)
        self.workspace = workspace
        self.event_bus = event_bus
        self.command_history = command_history
        self._drag_commands = []  # Commands collected during drag
        self._drag_start_point = None  # Starting point of current drag
    
    def on_click(self, point: Point) -> None:
        """Erase object at point."""
        cell = self.workspace.tilemap.get_cell(point.x, point.y)
        if not cell or not cell.map_object:
            return
        
        if self.command_history:
            # Use command pattern for undo/redo
            command = RemoveObjectCommand(self.workspace, point)
            self.command_history.execute(command)
        else:
            # Fallback to direct execution
            obj = cell.map_object
            # Find and remove from layer
            for layer in self.workspace.layers:
                if obj.id in [o.id for o in layer.get_map_objects()]:
                    layer.remove_map_object(obj.id)
                    break
            
            cell.clear()
        
        self.event_bus.publish(MapObjectErased(point, None))
    
    def on_drag_start(self, start: Point) -> None:
        """Start drag operation."""
        self._drag_start_point = start
        self._drag_commands = []
        # Erase object at start point - execute immediately for visual feedback
        cell = self.workspace.tilemap.get_cell(start.x, start.y)
        if cell and cell.map_object:
            command = RemoveObjectCommand(self.workspace, start)
            command.execute()  # Execute immediately for visual feedback
            self._drag_commands.append(command)
            self.event_bus.publish(MapObjectErased(start, None))
    
    def on_drag(self, start: Point, end: Point) -> None:
        """Erase objects along path during drag."""
        if self._drag_start_point is None:
            self._drag_start_point = start
        
        points = self._get_line_points(start, end)
        # Skip first point as it's already processed
        if len(points) > 1:
            points = points[1:]
        
        # Execute commands immediately for visual feedback, but collect them for undo
        for point in points:
            cell = self.workspace.tilemap.get_cell(point.x, point.y)
            if cell and cell.map_object:
                command = RemoveObjectCommand(self.workspace, point)
                command.execute()  # Execute immediately for visual feedback
                self._drag_commands.append(command)
                self.event_bus.publish(MapObjectErased(point, None))
    
    def on_drag_end(self) -> None:
        """End drag operation and group all commands as one composite for undo."""
        if self.command_history and self._drag_commands:
            # Commands are already executed, just group them for undo/redo
            from editing.commands.composite_command import CompositeCommand
            composite = CompositeCommand(self._drag_commands)
            # Add to history without executing (commands are already executed)
            self.command_history.add_executed_command(composite)
        
        # Reset drag state
        self._drag_commands = []
        self._drag_start_point = None
    
    def _get_line_points(self, start: Point, end: Point) -> list:
        """Get points on line."""
        points = []
        x0, y0 = start.x, start.y
        x1, y1 = end.x, end.y
        
        dx = abs(x1 - x0)
        dy = abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx - dy
        
        x, y = x0, y0
        while True:
            points.append(Point(x, y))
            if x == x1 and y == y1:
                break
            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x += sx
            if e2 < dx:
                err += dx
                y += sy
        
        return points

