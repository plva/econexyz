"""In-memory implementation of :class:`MessageBus`."""

import threading
import time
import logging
from collections import defaultdict
from typing import Callable, Dict, Any, List

from .base import MessageBus


class InMemoryMessageBus(MessageBus):
    """Simple in-memory message bus for local development."""

    def __init__(self) -> None:
        self.subscribers: Dict[str, List[Callable[[Dict[str, Any]], None]]] = defaultdict(list)
        self.messages: List[Dict[str, Any]] = []
        self._lock = threading.Lock()

    def publish(self, topic: str, message: Dict[str, Any]) -> None:
        logging.info("Publishing to %s: %s", topic, message)
        with self._lock:
            self.messages.append({"topic": topic, "message": message, "ts": time.time()})
        for callback in list(self.subscribers.get(topic, [])):
            callback(message)

    def subscribe(self, topic: str, callback: Callable[[Dict[str, Any]], None]) -> None:
        logging.info("Subscribed callback to topic %s", topic)
        self.subscribers[topic].append(callback)

    def get_messages(self) -> List[Dict[str, Any]]:
        """Return a snapshot of recent messages."""
        with self._lock:
            return list(self.messages)
