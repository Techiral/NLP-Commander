import re
from datetime import datetime, timedelta
from typing import Dict, Any

class NLPService:
    def process_command(self, command: str) -> Dict[str, Any]:
        """
        Processes natural language commands into structured intents.
        This version dynamically extracts the date (if 'tomorrow' is mentioned)
        and time from the command.
        """
        # Check if command is about scheduling or meeting
        if "schedule" in command.lower() or "meeting" in command.lower():
            # Compute date
            if "tomorrow" in command.lower():
                date_str = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
            else:
                date_str = datetime.now().strftime("%Y-%m-%d")  # fallback to today if needed

            # Use regex to find time patterns like "5 pm" or "5:30 pm"
            time_match = re.search(r'(\d{1,2})(?::(\d{2}))?\s*(am|pm)', command, re.IGNORECASE)
            if time_match:
                hour = int(time_match.group(1))
                minute = time_match.group(2) if time_match.group(2) else "00"
                period = time_match.group(3).upper()
                time_str = f"{hour}:{minute} {period}"
            else:
                time_str = "10:00 AM"  # fallback if no time is found

            return {
                "service": "calendar",
                "action": "create_event",
                "parameters": {
                    "title": "Team Meeting",
                    "date": date_str,
                    "time": time_str
                }
            }
        
        return {
            "service": "unknown",
            "action": "unknown",
            "parameters": {}
        }
