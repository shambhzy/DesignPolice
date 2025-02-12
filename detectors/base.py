from abc import ABC, abstractmethod
from typing import List, Dict

class BaseSmellDetector(ABC):
    @abstractmethod
    async def detect(self, code: str, file_path: str) -> List[Dict]:
        pass