"""Agent that periodically publishes local weather information."""

import time
from threading import Event
from typing import Optional
import logging

import requests

from .base import Agent


class WeatherAgent(Agent):
    """Fetches weather data from wttr.in and publishes it."""

    def __init__(self, name: str, bus, store, location: str = "", interval: float = 600.0):
        super().__init__(name, bus, store)
        self.location = location
        self.interval = interval
        self._stop_event = Event()

    def _get_weather(self) -> Optional[str]:
        try:
            url = f"https://wttr.in/{self.location}?format=3"
            resp = requests.get(url, timeout=10)
            if resp.status_code == 200:
                return resp.text.strip()
            logging.error("Weather request failed: %s", resp.status_code)
        except Exception as exc:  # pylint: disable=broad-except
            logging.exception("Error fetching weather: %s", exc)
        return None

    def run(self) -> None:
        """Periodically fetch and publish weather info."""
        while self.running and not self._stop_event.is_set():
            weather = self._get_weather()
            if weather:
                message = {"agent": self.name, "weather": weather}
                self.bus.publish("weather", message)
                logging.info("Published weather: %s", weather)
            time.sleep(self.interval)

    def shutdown(self) -> None:
        super().shutdown()
        self._stop_event.set()
