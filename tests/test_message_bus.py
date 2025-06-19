from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))

from econexyz.message_bus.in_memory import InMemoryMessageBus

def test_publish_subscribe(tmp_path):
    bus = InMemoryMessageBus()
    received = []

    def handler(msg):
        received.append(msg)

    bus.subscribe("test", handler)
    bus.publish("test", {"foo": "bar"})

    assert received == [{"foo": "bar"}]
    messages = bus.get_messages()
    assert messages[0]["message"] == {"foo": "bar"}
