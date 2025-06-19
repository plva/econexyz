"""Script to run EcoNexyz agents locally."""

import threading
import time
from pathlib import Path
import sys
import os
import logging

# Allow running without installation
sys.path.append(str(Path(__file__).resolve().parents[1]))

from econexyz.agents.sample import SampleAgent
from econexyz.message_bus.in_memory import InMemoryMessageBus
from econexyz.storage.sqlite_store import SQLiteKnowledgeStore
from dashboard.api import state


def main() -> None:
    log_dir = os.path.expanduser("~/tmp")
    os.makedirs(log_dir, exist_ok=True)
    logging.basicConfig(
        filename=os.path.join(log_dir, "econexyz.log"),
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
    )

    bus = InMemoryMessageBus()
    with SQLiteKnowledgeStore() as store:
        agent = SampleAgent("sample-agent", bus, store)

        # expose state to dashboard
        state.message_bus = bus
        state.agents.append(agent)

        agent.setup()
        thread = threading.Thread(target=agent.run, daemon=True)
        thread.start()

        try:
            while thread.is_alive():
                time.sleep(0.5)
        except KeyboardInterrupt:
            agent.shutdown()
            thread.join()


if __name__ == "__main__":
    main()
