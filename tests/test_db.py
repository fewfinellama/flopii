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

def test_db_mid_flight_deletion(tmp_path):
    import core.db
    import os
    
    test_db = str(tmp_path / "test_agent_state_robust.db")
    core.db.DB_PATH = test_db

    # Standard initialization
    core.db.init_db()
    core.db.set_setting("key1", "val1")
    assert core.db.get_setting("key1") == "val1"

    # Simulate user deleting the DB file while the server is running
    os.remove(test_db)
    assert not os.path.exists(test_db)

    # Attempt to write a new setting. Our robust DB layer should 
    # catch the missing table error, instantly recreate the DB/tables, and succeed.
    core.db.set_setting("key2", "val2")
    
    # Verify the file was recreated and data is accessible
    assert os.path.exists(test_db)
    assert core.db.get_setting("key2") == "val2"
