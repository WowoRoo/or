"""Workspace service."""

from typing import Optional
from domain.entities.workspace import Workspace
from domain.value_objects.references import TileListReference, FunctionalTileListReference
from core.events.event_bus import EventBus
from core.events.domain_events import WorkspaceCreated, WorkspaceSaved, WorkspaceLoaded


class WorkspaceService:
    """Service for managing workspaces."""
    
    def __init__(self, event_bus: EventBus):
        self.event_bus = event_bus
        self.current_workspace: Optional[Workspace] = None
    
    def create_workspace(
        self,
        name: str,
        author: str,
        width: int,
        height: int,
        tile_list_reference: TileListReference,
        functional_tile_list_reference: FunctionalTileListReference
    ) -> Workspace:
        """Create new workspace."""
        workspace = Workspace.create_new(
            name, author, width, height,
            tile_list_reference, functional_tile_list_reference
        )
        self.current_workspace = workspace
        self.event_bus.publish(WorkspaceCreated(workspace.id))
        return workspace
    
    def get_current_workspace(self) -> Optional[Workspace]:
        """Get current workspace."""
        return self.current_workspace
    
    def set_current_workspace(self, workspace: Workspace) -> None:
        """Set current workspace."""
        self.current_workspace = workspace

