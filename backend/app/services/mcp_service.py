from typing import List, Dict, Any
from ..adapters.base_adapter import BaseAdapter

class MCPService:
    def __init__(self, adapters: List[BaseAdapter]):
        self.adapters = {adapter.service_name: adapter for adapter in adapters}
    
    def process_intent(self, intent: Dict[str, Any]) -> bool:
        service = intent.get("service")
        if service not in self.adapters:
            return False
        
        adapter = self.adapters[service]
        return adapter.execute(intent)