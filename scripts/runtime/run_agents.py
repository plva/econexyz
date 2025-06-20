"""Script to run EcoNexyz agents locally."""

import threading
import time
from pathlib import Path
import sys
import os
import logging
from typing import Optional

import uvicorn

# Allow running without installation
sys.path.append(str(Path(__file__).resolve().parents[1]))

from econexyz.agents.sample import SampleAgent
from econexyz.message_bus.in_memory import InMemoryMessageBus
from econexyz.storage.sqlite_store import SQLiteKnowledgeStore
from dashboard.api import state


def main(start_dashboard: bool = True) -> None:
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
        agent_thread = threading.Thread(target=agent.run, daemon=True)
        agent_thread.start()

        server: Optional[uvicorn.Server] = None
        server_thread: Optional[threading.Thread] = None

        if start_dashboard:
            config = uvicorn.Config("dashboard.api.main:app", host="127.0.0.1", port=8000)
            server = uvicorn.Server(config)
            server_thread = threading.Thread(target=server.run, daemon=True)
            server_thread.start()

        try:
            while agent_thread.is_alive() and (server_thread is None or server_thread.is_alive()):
                time.sleep(0.5)
        except KeyboardInterrupt:
            agent.shutdown()
            if server is not None:
                server.should_exit = True

        agent_thread.join()
        if server_thread is not None:
            server_thread.join()


if __name__ == "__main__":
    main()
