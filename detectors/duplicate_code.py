from .base import BaseSmellDetector
from services.gemini_service import GeminiAdapter
from typing import List, Dict

class DuplicateCodeDetector(BaseSmellDetector):
    def __init__(self, gemini_adapter: GeminiAdapter):
        self.gemini = gemini_adapter

    async def detect(self, code: str, file_path: str) -> List[Dict]:
        prompt = f"""Analyze this code for duplicate code patterns:
        {code}
        
        Identify:
        1. Repeated code blocks
        2. Similar methods with minor variations
        3. Copy-pasted code segments
        
        Format: Return a JSON list of issues with 'description' and 'suggested_fix'
        """
        return await self.gemini.analyze_code(prompt)