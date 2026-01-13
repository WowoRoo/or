"""Functional tile type enumeration."""

from enum import Enum


class FunctionalTileType(Enum):
    """Type of functional tile."""
    PLAYER_START = "player_start"
    ENEMY = "enemy"
    CHECKPOINT = "checkpoint"
    COIN = "coin"
    POWERUP = "powerup"
    EXIT = "exit"

