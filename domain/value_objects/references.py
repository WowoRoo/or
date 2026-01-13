"""Reference value objects for tile lists."""

from dataclasses import dataclass
from typing import List, Optional
from domain.enums.tile_type import TileType
from domain.enums.functional_tile_type import FunctionalTileType


@dataclass(frozen=True)
class TileListReference:
    """Reference to available tile types."""
    tile_types: List[TileType]
    
    def get_tile_type(self, name: str) -> Optional[TileType]:
        """Get tile type by name."""
        for tile_type in self.tile_types:
            if tile_type.value == name:
                return tile_type
        return None


@dataclass(frozen=True)
class FunctionalTileListReference:
    """Reference to available functional tile types."""
    functional_tile_types: List[FunctionalTileType]
    
    def get_functional_tile_type(self, name: str) -> Optional[FunctionalTileType]:
        """Get functional tile type by name."""
        for tile_type in self.functional_tile_types:
            if tile_type.value == name:
                return tile_type
        return None

