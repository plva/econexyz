from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))

if 'requests' not in sys.modules:
    sys.modules['requests'] = type('Dummy', (), {})()

from dashboard.api.main import get_messages
from dashboard.api import state
from econexyz.message_bus.in_memory import InMemoryMessageBus


def test_messages_pagination():
    bus = InMemoryMessageBus()
    state.message_bus = bus
    for i in range(60):
        bus.publish("test", {"num": i})

    data = get_messages()
    assert data["page"] == 1
    assert data["page_size"] == 50
    assert data["total"] == 60
    assert len(data["messages"]) == 50
    assert data["messages"][0]["message"]["num"] == 59
    assert data["messages"][-1]["message"]["num"] == 10

    data = get_messages(page=2)
    assert data["page"] == 2
    assert len(data["messages"]) == 10
    assert data["messages"][0]["message"]["num"] == 9
    assert data["messages"][-1]["message"]["num"] == 0

    state.message_bus = None
