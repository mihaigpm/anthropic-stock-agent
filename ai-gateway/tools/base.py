from abc import ABC, abstractmethod
from typing import Any, Dict

class BaseTool(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @property
    @abstractmethod
    def definition(self) -> Dict[str, Any]:
        """The JSON schema sent to Claude"""
        pass

    @abstractmethod
    async def execute(self, **kwargs) -> Any:
        pass