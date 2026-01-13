"""Dependency Injection container."""

from typing import Dict, Type, TypeVar, Callable, Any, Optional
import inspect

T = TypeVar('T')


class DIContainer:
    """Simple dependency injection container."""
    
    def __init__(self):
        self._services: Dict[Type, Any] = {}
        self._factories: Dict[Type, Callable] = {}
        self._singletons: Dict[Type, Any] = {}
    
    def register(self, service_type: Type[T], implementation: T) -> None:
        """Register service instance."""
        self._services[service_type] = implementation
    
    def register_factory(self, service_type: Type[T], factory: Callable[[], T]) -> None:
        """Register factory function."""
        self._factories[service_type] = factory
    
    def register_singleton(self, service_type: Type[T], factory: Callable[[], T]) -> None:
        """Register singleton factory."""
        self._factories[service_type] = factory
        self._singletons[service_type] = None
    
    def resolve(self, service_type: Type[T]) -> T:
        """Resolve service instance."""
        # Check if already registered
        if service_type in self._services:
            return self._services[service_type]
        
        # Check if singleton exists
        if service_type in self._singletons:
            if self._singletons[service_type] is None:
                self._singletons[service_type] = self._factories[service_type]()
            return self._singletons[service_type]
        
        # Check if factory exists
        if service_type in self._factories:
            instance = self._factories[service_type]()
            if service_type in self._singletons:
                self._singletons[service_type] = instance
            return instance
        
        # Try to auto-resolve with constructor injection
        try:
            sig = inspect.signature(service_type.__init__)
            params = {}
            for param_name, param in sig.parameters.items():
                if param_name == 'self':
                    continue
                if param.annotation != inspect.Parameter.empty:
                    params[param_name] = self.resolve(param.annotation)
            
            return service_type(**params)
        except Exception:
            raise ValueError(f"Cannot resolve {service_type}")
    
    def configure(self) -> None:
        """Configure container with default modules."""
        from core.di.modules import configure_modules
        configure_modules(self)

