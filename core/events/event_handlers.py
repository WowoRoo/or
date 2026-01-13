"""Event handlers."""

from typing import Callable
from core.events.domain_events import DomainEvent


class EventHandler:
    """Base event handler."""
    
    def handle(self, event: DomainEvent) -> None:
        """Handle event."""
        raise NotImplementedError


def event_handler(event_type: type) -> Callable:
    """Decorator for event handlers."""
    def decorator(func: Callable) -> Callable:
        func._event_type = event_type
        return func
    return decorator

