"""SQLite-backed implementation of :class:`KnowledgeStore`."""

import json
import sqlite3
from typing import Dict, Any

from .base import KnowledgeStore


class SQLiteKnowledgeStore(KnowledgeStore):
    """Persist knowledge using a local SQLite database."""

    def __init__(self, path: str = "knowledge.db") -> None:
        self.conn = sqlite3.connect(path)
        self._create_table()

    def _create_table(self) -> None:
        cur = self.conn.cursor()
        cur.execute(
            "CREATE TABLE IF NOT EXISTS store (key TEXT PRIMARY KEY, data TEXT)"
        )
        self.conn.commit()

    def save(self, key: str, data: Dict[str, Any]) -> None:
        cur = self.conn.cursor()
        cur.execute(
            "REPLACE INTO store (key, data) VALUES (?, ?)",
            (key, json.dumps(data)),
        )
        self.conn.commit()

    def load(self, key: str) -> Dict[str, Any]:
        cur = self.conn.cursor()
        cur.execute("SELECT data FROM store WHERE key = ?", (key,))
        row = cur.fetchone()
        if row:
            return json.loads(row[0])
        return {}
