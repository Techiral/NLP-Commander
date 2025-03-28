from typing import Dict, Any
from .base_adapter import BaseAdapter

class CalendarAdapter(BaseAdapter):
    @property
    def service_name(self) -> str:
        return "calendar"
    
    def execute(self, intent: Dict[str, Any]) -> bool:
        if intent["action"] != "create_event":
            return False
        
        params = intent["parameters"]
        print(f"Creating calendar event: {params['title']} on {params['date']} at {params['time']}")
        return True