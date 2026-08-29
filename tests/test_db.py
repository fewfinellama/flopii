import os
import pytest


def test_db_operations(tmp_path):
    import core.db

    # Redirect DB path to a temporary test file
    test_db = str(tmp_path / "test_agent_state.db")
    core.db.DB_PATH = test_db

    core.db.init_db()
    core.db.set_setting("test_key", "test_value")

    assert core.db.get_setting("test_key") == "test_value"
    assert core.db.get_setting("nonexistent") is None
