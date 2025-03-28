# NLP Command Processor

A FastAPI-based backend system that processes natural language commands into structured actions for SaaS services.

## Features

- Natural language command processing
- Modular adapter architecture for service integration
- API key authentication
- Command status tracking
- Extensible design for adding new service adapters

## Project Structure

```
backend/
├── app/
│   ├── adapters/         # Service adapters
│   ├── models/          # Data models
│   ├── services/        # Core services
│   └── main.py         # FastAPI application
├── tests/              # Unit tests
└── requirements.txt    # Python dependencies
```

## Setup

1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the server:
   ```bash
   uvicorn app.main:app --reload
   ```

## API Documentation

Once the server is running, visit:
- OpenAPI documentation: http://localhost:8000/docs
- ReDoc documentation: http://localhost:8000/redoc

## Authentication

All endpoints require an API key header:
```
X-API-Key: your-secret-key
```

## Endpoints

### POST /process-command

Process a natural language command.

Request:
```json
{
  "command": "Schedule a team meeting"
}
```

Response:
```json
{
  "command_id": "20250401100000",
  "status": "completed",
  "processed_intent": {
    "service": "calendar",
    "action": "create_event",
    "parameters": {
      "title": "Team Meeting",
      "date": "2025-04-01",
      "time": "10:00 AM"
    }
  }
}
```

### GET /status/{command_id}

Get the status of a processed command.

## Extending the Adapter Layer

To add a new service adapter:

1. Create a new adapter class in `app/adapters/` that inherits from `BaseAdapter`
2. Implement the required methods:
   - `service_name` property
   - `execute()` method
3. Register the adapter in `MCPService` initialization

Example:
```python
class EmailAdapter(BaseAdapter):
    @property
    def service_name(self) -> str:
        return "email"
    
    def execute(self, intent: Dict[str, Any]) -> bool:
        # Implement email sending logic
        return True
```

## Running Tests

```bash
pytest
```