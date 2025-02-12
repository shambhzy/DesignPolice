from .base import BaseSmellDetector
from services.gemini_service import GeminiAdapter
from typing import List, Dict

class LargeClassDetector(BaseSmellDetector):
    def __init__(self, gemini_adapter: GeminiAdapter):
        self.gemini = gemini_adapter

    async def detect(self, code: str, file_path: str) -> List[Dict]:
        prompt = f"""Analyze this code for the Large Class smell:
        {code}
        
        Return only classes that:
        1. Have too many responsibilities
        2. Have too many methods or lines of code
        3. Could be split into smaller, more focused classes
        
        Format: Return a JSON list of issues with 'description' and 'suggested_fix'
        """
        return await self.gemini.analyze_code(prompt)