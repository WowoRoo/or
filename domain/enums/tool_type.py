"""Tool type enumeration."""

from enum import Enum


class ToolType(Enum):
    """Type of editing tool."""
    BRUSH = "brush"
    ERASER = "eraser"
    FLOOD = "flood"
    TRASH = "trash"
    TEMPLATE = "template"

