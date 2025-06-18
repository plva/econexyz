"""Global state shared with the dashboard API."""

from typing import List, Optional

from econexyz.agents.base import Agent
from econexyz.message_bus.base import MessageBus

# Message bus instance used by running agents
message_bus: Optional[MessageBus] = None

# List of running agents
agents: List[Agent] = []
