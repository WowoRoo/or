"""Map object type enumeration."""

from enum import Enum


class MapObjectType(Enum):
    """Type of map object."""
    TILE = "tile"
    FUNCTIONAL_TILE = "functional_tile"

