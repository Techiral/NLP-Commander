from abc import ABC, abstractmethod
from typing import Dict, Any

class BaseAdapter(ABC):
    @property
    @abstractmethod
    def service_name(self) -> str:
        pass
    
    @abstractmethod
    def execute(self, intent: Dict[str, Any]) -> bool:
        pass