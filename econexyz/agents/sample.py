"""Sample agent demonstrating periodic message publishing."""

import time
from threading import Event
import logging

from .base import Agent


class SampleAgent(Agent):
    """Agent that periodically publishes messages to a topic."""

    def __init__(self, name: str, bus, store, interval: float = 2.0):
        super().__init__(name, bus, store)
        self.interval = interval
        self._stop_event = Event()

    def run(self) -> None:
        """Run a simple loop publishing incrementing counters."""
        counter = 0
        while self.running and not self._stop_event.is_set():
            message = {"agent": self.name, "counter": counter}
            self.bus.publish("sample", message)
            logging.info("%s published %s", self.name, message)
            counter += 1
            time.sleep(self.interval)

    def shutdown(self) -> None:
        super().shutdown()
        self._stop_event.set()
