"""Base command class."""

from abc import ABC, abstractmethod


class Command(ABC):
    """Base class for commands."""
    
    @abstractmethod
    def execute(self) -> None:
        """Execute command."""
        pass
    
    @abstractmethod
    def undo(self) -> None:
        """Undo command."""
        pass

