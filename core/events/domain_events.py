"""Domain events definitions."""

from abc import ABC
from uuid import UUID
from typing import Optional
from domain.value_objects.point import Point
from domain.enums.tool_type import ToolType
from domain.enums.skeletonization_algorithm import SkeletonizationAlgorithm


class DomainEvent(ABC):
    """Base class for domain events."""
    pass


# Workspace Events
class WorkspaceCreated(DomainEvent):
    """Workspace was created."""
    def __init__(self, workspace_id: UUID):
        self.workspace_id = workspace_id


class WorkspaceLoaded(DomainEvent):
    """Workspace was loaded."""
    def __init__(self, workspace_id: UUID):
        self.workspace_id = workspace_id


class WorkspaceSaved(DomainEvent):
    """Workspace was saved."""
    def __init__(self, workspace_id: UUID):
        self.workspace_id = workspace_id


class LayerAdded(DomainEvent):
    """Layer was added."""
    def __init__(self, layer_id: UUID):
        self.layer_id = layer_id


class LayerRemoved(DomainEvent):
    """Layer was removed."""
    def __init__(self, layer_id: UUID):
        self.layer_id = layer_id


class LayerSwitched(DomainEvent):
    """Active layer was switched."""
    def __init__(self, layer_id: UUID):
        self.layer_id = layer_id


class TilePlaced(DomainEvent):
    """Tile was placed."""
    def __init__(self, position: Point, tile_id: UUID):
        self.position = position
        self.tile_id = tile_id


class MapObjectErased(DomainEvent):
    """Map object was erased."""
    def __init__(self, position: Point, object_id: UUID):
        self.position = position
        self.object_id = object_id


class BerlinWallDetected(DomainEvent):
    """Berlin wall was detected."""
    def __init__(self, min_x: int, min_y: int, max_x: int, max_y: int):
        self.min_x = min_x
        self.min_y = min_y
        self.max_x = max_x
        self.max_y = max_y


# Tool Events
class ToolActivated(DomainEvent):
    """Tool was activated."""
    def __init__(self, tool_type: ToolType):
        self.tool_type = tool_type


class RegionFilled(DomainEvent):
    """Region was filled."""
    def __init__(self, region_size: int):
        self.region_size = region_size


# Biometric Events
class PreprocessingCompleted(DomainEvent):
    """Preprocessing completed."""
    pass


class ZaborizationCompleted(DomainEvent):
    """Zaborization completed."""
    pass


class WorkspaceBitmapGenerated(DomainEvent):
    """Workspace bitmap was generated."""
    pass


class SkeletonGenerated(DomainEvent):
    """Skeleton was generated."""
    def __init__(self, algorithm: SkeletonizationAlgorithm):
        self.algorithm = algorithm


class CrossinizerComputed(DomainEvent):
    """Crossinizer computed."""
    pass


class FeaturesDetected(DomainEvent):
    """Features were detected."""
    def __init__(self, count: int):
        self.count = count


class FeaturesVectorCreated(DomainEvent):
    """Features vector was created."""
    pass

