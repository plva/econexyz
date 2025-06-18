"""Message bus interface for pub/sub communication."""

from abc import ABC, abstractmethod
from typing import Callable, Dict, Any


class MessageBus(ABC):
    """Abstract publish/subscribe bus."""

    @abstractmethod
    def publish(self, topic: str, message: Dict[str, Any]) -> None:
        """Publish a message to a topic."""
        raise NotImplementedError

    @abstractmethod
    def subscribe(self, topic: str, callback: Callable[[Dict[str, Any]], None]) -> None:
        """Subscribe to a topic with a callback."""
        raise NotImplementedError
