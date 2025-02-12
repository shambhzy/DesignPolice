from .base import BaseRefactoringStrategy
from services.gemini_service import GeminiAdapter
from typing import Dict

class RemoveDuplicationStrategy(BaseRefactoringStrategy):
    def __init__(self, gemini_adapter: GeminiAdapter):
        self.gemini = gemini_adapter

    async def refactor(self, issue, code) -> str:
        prompt = f"""Refactor this code to remove duplication:
        Issue: {issue['description']}
        
        Original Code:
        {code}
        
        Requirements:
        1. Extract common functionality into reusable methods
        2. Use inheritance or composition where appropriate
        3. Maintain code readability
        4. Add proper documentation
        
        Return only the refactored code.
        """
        return await self.gemini.analyze_code(prompt)