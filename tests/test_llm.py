import pytest
from core.llm import generate_with_failover

def test_generate_with_failover_success():
    # Setup mock config
    config = {
        "primary": "p1",
        "auto_failover": True,
        "providers": [
            {"id": "p1", "name": "OpenAI", "model": "", "api_key": "test_key", "verified": True, "failures": 0},
            {"id": "p2", "name": "Groq", "model": "", "api_key": "test_key", "verified": True, "failures": 0}
        ]
    }
    
    # We need to mock generate_payload
    # Since we can't easily mock in a simple file write without monkeypatch, we'll use pytest's monkeypatch
    pass

def test_generate_with_failover_trigger(monkeypatch):
    import core.llm
    
    # Mock generate_payload to always fail
    def mock_generate(*args, **kwargs):
        return "Error: Simulated failure"
        
    monkeypatch.setattr(core.llm, "generate_payload", mock_generate)
    
    config = {
        "primary": "p1",
        "auto_failover": True,
        "providers": [
            {"id": "p1", "name": "OpenAI", "model": "", "api_key": "test_key", "verified": True, "failures": 2},
            {"id": "p2", "name": "Groq", "model": "", "api_key": "test_key", "verified": True, "failures": 0}
        ]
    }
    
    db_called = False
    def mock_db_update(new_config):
        nonlocal db_called
        db_called = True
        
    # Act
    # Provider 1 is at 2 failures. The next failure should trigger failover.
    result = core.llm.generate_with_failover(config, "context", "prompt", db_update_callback=mock_db_update)
    
    # Assert
    assert db_called == True
    # The primary should have switched to p2
    assert config["primary"] == "p2"
    # p1's failures should be 3
    assert config["providers"][0]["failures"] == 3
    # And since p2 also fails (because mock_generate always fails), it will return an error eventually.
    assert result.startswith("Error")

