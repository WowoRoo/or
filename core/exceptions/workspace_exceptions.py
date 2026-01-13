"""Workspace-related exceptions."""


class WorkspaceException(Exception):
    """Base exception for workspace operations."""
    pass


class WorkspaceNotFoundError(WorkspaceException):
    """Workspace not found."""
    pass


class InvalidWorkspaceSizeError(WorkspaceException):
    """Invalid workspace size."""
    pass


class LayerNotFoundError(WorkspaceException):
    """Layer not found."""
    pass

