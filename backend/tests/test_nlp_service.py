import pytest
from app.services.nlp_service import NLPService

def test_process_command_meeting():
    nlp_service = NLPService()
    result = nlp_service.process_command("Schedule a team meeting")
    
    assert result["service"] == "calendar"
    assert result["action"] == "create_event"
    assert "title" in result["parameters"]
    assert "date" in result["parameters"]
    assert "time" in result["parameters"]

def test_process_command_unknown():
    nlp_service = NLPService()
    result = nlp_service.process_command("Do something random")
    
    assert result["service"] == "unknown"
    assert result["action"] == "unknown"
    assert result["parameters"] == {}