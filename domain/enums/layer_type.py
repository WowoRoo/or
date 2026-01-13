"""Layer type enumeration."""

from enum import Enum


class LayerType(Enum):
    """Type of layer in workspace."""
    TILE_LAYER = "tile_layer"
    FUNCTIONAL_TILE_LAYER = "functional_tile_layer"

