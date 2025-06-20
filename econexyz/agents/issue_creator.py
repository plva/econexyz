"""Agent that creates issue files from short descriptions."""

from __future__ import annotations

import logging
from datetime import date
import time
from pathlib import Path
from typing import Dict, Any, Optional

from econexyz.message_bus.base import MessageBus
from econexyz.storage.base import KnowledgeStore
from .base import Agent

import sys
ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(ROOT))
from scripts import create_issue


class SmartIssueCreatorAgent(Agent):
    """Generate issue files from simple requests."""

    def __init__(
        self,
        name: str,
        bus: MessageBus,
        store: KnowledgeStore,
        config_path: Optional[Path] = None,
    ) -> None:
        super().__init__(name, bus, store)
        self.config_path = config_path or Path(__file__).resolve().parents[2] / "config" / "issue_categories.yml"
        self.categories = create_issue.load_categories()
        self.bus.subscribe("issue_request", self.handle_request)

    def run(self) -> None:
        """Idle loop waiting for messages."""
        logging.info("%s listening for issue requests", self.name)
        while self.running:
            time.sleep(0.1)

    def _choose_category(self, description: str) -> str:
        """Return a category based on simple heuristics."""
        text = description.lower()
        if "bug" in text or "error" in text:
            return "bugs"
        if "dashboard" in text:
            return "dashboard"
        if "agent" in text:
            return "agents"
        if "bus" in text:
            return "bus"
        return "workflow"

    def handle_request(self, message: Dict[str, Any]) -> None:
        """Process an issue creation request message."""
        desc = message.get("description", "").strip()
        if not desc:
            logging.warning("%s received empty description", self.name)
            return

        category = message.get("category") or self._choose_category(desc)
        tags = message.get("tags") or self.categories.get(category, {}).get("tags", [])
        priority = message.get("priority", "medium")

        name = "_".join(desc.lower().split())[:30]
        today = date.today().isoformat()
        content = create_issue.render_content(category, name, tags, priority, today)
        print(content)
        approve = input("Create this issue? [y/N] ")
        if approve.lower().startswith("y"):
            create_issue.create_issue(category, name, tags=tags, priority=priority)
            self.store.save(name, {"category": category, "created": today})
            logging.info("%s created issue %s/%s", self.name, category, name)
        else:
            logging.info("%s cancelled issue creation", self.name)

