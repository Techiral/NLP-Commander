from pydantic import BaseModel
from typing import Dict, Any, Optional
from datetime import datetime

class Command(BaseModel):
    id: str
    raw_command: str
    processed_intent: Dict[str, Any]
    timestamp: datetime = datetime.now()

class CommandStatus(BaseModel):
    command_id: str
    status: str
    processed_intent: Optional[Dict[str, Any]] = None
    timestamp: datetime = datetime.now()