"""Agent base class defining lifecycle methods."""

from abc import ABC, abstractmethod
import logging

from econexyz.message_bus.base import MessageBus
from econexyz.storage.base import KnowledgeStore


class Agent(ABC):
    """Base interface for autonomous agents."""

    def __init__(self, name: str, bus: MessageBus, store: KnowledgeStore):
        self.name = name
        self.bus = bus
        self.store = store
        self.running = False

    def setup(self) -> None:
        """Initialize resources before running."""
        self.running = True
        logging.info("Agent %s setup", self.name)

    @abstractmethod
    def run(self) -> None:
        """Main loop for the agent. Implement autonomous logic here."""
        raise NotImplementedError

    def shutdown(self) -> None:
        """Clean up resources when the agent stops."""
        self.running = False
        logging.info("Agent %s shutting down", self.name)
