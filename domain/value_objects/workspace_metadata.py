"""Workspace metadata value object."""

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class WorkspaceMetadata:
    """Metadata for workspace."""
    name: str
    author: str
    created_at: datetime
    modified_at: datetime
    width: int
    height: int

