from typing import List
import os

class FileHandler:
    @staticmethod
    def is_supported_file(filename: str, supported_extensions: List[str]) -> bool:
        return any(filename.endswith(ext) for ext in supported_extensions)

    @staticmethod
    def get_file_size(content: str) -> int:
        return len(content.encode('utf-8'))