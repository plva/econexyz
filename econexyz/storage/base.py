"""Knowledge store interface."""

from abc import ABC, abstractmethod
from typing import Dict, Any


class KnowledgeStore(ABC):
    """Abstract persistence layer."""

    @abstractmethod
    def save(self, key: str, data: Dict[str, Any]) -> None:
        """Persist data by key."""
        raise NotImplementedError

    @abstractmethod
    def load(self, key: str) -> Dict[str, Any]:
        """Load data by key."""
        raise NotImplementedError
