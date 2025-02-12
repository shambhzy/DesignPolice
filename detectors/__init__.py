
from .duplicate_code import DuplicateCodeDetector
from services.gemini_service import GeminiAdapter
from .large_classes import LargeClassDetector
from .base import BaseSmellDetector

class SmellDetectorFactory:
    def __init__(self, gemini_adapter: GeminiAdapter):
        self.gemini_adapter = gemini_adapter

    def get_detector(self, smell_type: str) -> BaseSmellDetector:
        detectors = {
            "large_class": LargeClassDetector(self.gemini_adapter),
            "duplicate_code": DuplicateCodeDetector(self.gemini_adapter)
        }
        return detectors.get(smell_type)