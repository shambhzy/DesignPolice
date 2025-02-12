from abc import ABC, abstractmethod
from typing import Dict, Any

class BaseRefactoringStrategy(ABC):
    @abstractmethod
    async def refactor(self, issue: Dict[str, Any], code: str) -> str:
        pass