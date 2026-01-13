"""Base tool class."""

from abc import ABC, abstractmethod
from domain.value_objects.point import Point
from domain.enums.tool_type import ToolType


class BaseTool(ABC):
    """Base class for editing tools."""
    
    def __init__(self, tool_type: ToolType):
        self.tool_type = tool_type
    
    @abstractmethod
    def on_click(self, point: Point) -> None:
        """Handle click at point."""
        pass
    
    @abstractmethod
    def on_drag(self, start: Point, end: Point) -> None:
        """Handle drag from start to end."""
        pass

