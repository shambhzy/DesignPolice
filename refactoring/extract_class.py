from .base import BaseRefactoringStrategy
from services.gemini_service import GeminiAdapter


class ExtractClassStrategy(BaseRefactoringStrategy):
    def __init__(self, gemini_adapter: GeminiAdapter):
        self.gemini = gemini_adapter

    async def refactor(self, issue, code: str) -> str:
        prompt = f"""Refactor this code to fix the Large Class issue:
        Issue: {issue['description']}
        
        Original Code:
        {code}
        
        Requirements:
        1. Extract related methods and properties into new classes
        2. Maintain functionality and interfaces
        3. Follow SOLID principles
        4. Add proper documentation
        
        Return only the refactored code.
        """
        return await self.gemini.analyze_code(prompt)
