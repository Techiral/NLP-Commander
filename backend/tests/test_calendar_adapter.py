import pytest
from app.adapters.calendar_adapter import CalendarAdapter

def test_calendar_adapter_execute():
    adapter = CalendarAdapter()
    intent = {
        "service": "calendar",
        "action": "create_event",
        "parameters": {
            "title": "Test Meeting",
            "date": "2025-04-01",
            "time": "10:00 AM"
        }
    }
    
    assert adapter.execute(intent) == True

def test_calendar_adapter_invalid_action():
    adapter = CalendarAdapter()
    intent = {
        "service": "calendar",
        "action": "invalid_action",
        "parameters": {}
    }
    
    assert adapter.execute(intent) == False