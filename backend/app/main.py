from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import APIKeyHeader
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict, Any
import json
from datetime import datetime

from .services.nlp_service import NLPService
from .services.mcp_service import MCPService
from .models.command import Command, CommandStatus
from .adapters.calendar_adapter import CalendarAdapter

app = FastAPI(
    title="NLP Command Processor",
    description="A service that processes natural language commands into structured actions",
    version="1.0.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Frontend dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Simple API key authentication
API_KEY = "your-secret-key"  # In production, use environment variables
api_key_header = APIKeyHeader(name="X-API-Key")

def verify_api_key(api_key: str = Depends(api_key_header)):
    if api_key != API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key"
        )
    return api_key

# Initialize services
nlp_service = NLPService()
calendar_adapter = CalendarAdapter()
mcp_service = MCPService([calendar_adapter])

class CommandRequest(BaseModel):
    command: str

class CommandResponse(BaseModel):
    command_id: str
    status: str
    processed_intent: Optional[Dict[str, Any]] = None

# Store command history (replace with database in production)
command_history: Dict[str, CommandStatus] = {}

@app.post("/process-command", response_model=CommandResponse)
async def process_command(
    request: CommandRequest,
    api_key: str = Depends(verify_api_key)
):
    # Process the natural language command
    intent = nlp_service.process_command(request.command)
    
    # Create a command instance
    command = Command(
        id=datetime.now().strftime("%Y%m%d%H%M%S"),
        raw_command=request.command,
        processed_intent=intent
    )
    
    # Process the command through MCP
    result = mcp_service.process_intent(intent)
    
    # Store command status
    command_history[command.id] = CommandStatus(
        command_id=command.id,
        status="completed" if result else "failed",
        processed_intent=intent
    )
    
    return CommandResponse(
        command_id=command.id,
        status="completed" if result else "failed",
        processed_intent=intent
    )

@app.get("/status/{command_id}", response_model=CommandStatus)
async def get_status(
    command_id: str,
    api_key: str = Depends(verify_api_key)
):
    if command_id not in command_history:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Command not found"
        )
    return command_history[command_id]

# Remove the __main__ block that uses uvicorn directly
# Instead, we'll use the FastAPI app instance directly