"""Tile type enumeration."""

from enum import Enum


class TileType(Enum):
    """Type of tile."""
    GRASS = "grass"
    STONE = "stone"
    WATER = "water"
    DIRT = "dirt"
    SAND = "sand"
    SNOW = "snow"
    LAVA = "lava"

