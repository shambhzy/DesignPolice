# refactoring/__init__.py
from .extract_class import ExtractClassStrategy
from .remove_duplication import RemoveDuplicationStrategy
from services.gemini_service import GeminiAdapter
from typing import Optional
from .base import BaseRefactoringStrategy

class RefactoringStrategy:
    """
    Factory class for creating refactoring strategies based on the issue type.
    """
    def __init__(self, gemini_adapter: GeminiAdapter):
        self.gemini_adapter = gemini_adapter
        self.strategies = {
            "large_class": ExtractClassStrategy(gemini_adapter),
            "duplicate_code": RemoveDuplicationStrategy(gemini_adapter)
        }
    
    def get_strategy(self, issue_type: str) -> Optional[BaseRefactoringStrategy]:
        """
        Get the appropriate refactoring strategy based on the issue type.
        
        Args:
            issue_type: Type of code smell to be refactored
            
        Returns:
            Optional[BaseRefactoringStrategy]: The strategy instance or None if not found
        """
        # Map issue types to strategy types
        strategy_mapping = {
            "large_class": "large_class",
            "god_class": "large_class",  # Alias for large class
            "duplicate_code": "duplicate_code",
            "code_duplication": "duplicate_code",  # Alias for duplicate code
            # Add more mappings as needed
        }
        
        # Get the normalized strategy type
        strategy_type = strategy_mapping.get(issue_type.lower())
        
        # Return the strategy instance or None if not found
        return self.strategies.get(strategy_type)
    
    def register_strategy(self, issue_type: str, strategy: BaseRefactoringStrategy) -> None:
        """
        Register a new refactoring strategy.
        
        Args:
            issue_type: Type of code smell the strategy handles
            strategy: Strategy instance to register
        """
        self.strategies[issue_type] = strategy
        
__all__ = ['RefactoringStrategy', 'BaseRefactoringStrategy', 
           'ExtractClassStrategy', 'RemoveDuplicationStrategy']