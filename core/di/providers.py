"""Dependency providers."""

from typing import Callable, TypeVar

T = TypeVar('T')


class Provider:
    """Base provider class."""
    
    def get(self) -> T:
        """Get instance."""
        raise NotImplementedError


class FactoryProvider(Provider):
    """Provider using factory function."""
    
    def __init__(self, factory: Callable[[], T]):
        self.factory = factory
    
    def get(self) -> T:
        """Get instance from factory."""
        return self.factory()

