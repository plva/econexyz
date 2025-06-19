from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))

from econexyz.storage.sqlite_store import SQLiteKnowledgeStore


def test_save_load(tmp_path):
    db_path = tmp_path / "test.db"
    store = SQLiteKnowledgeStore(str(db_path))
    store.save("key", {"value": 1})
    result = store.load("key")
    assert result == {"value": 1}
    store.close()
