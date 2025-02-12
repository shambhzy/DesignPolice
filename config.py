
from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    github_token: str = ""
    github_repo: str = ""
    gemini_api_key: str = ''
    scan_interval: int = 3600
    github_base_url: str = "https://api.github.com"
    max_file_size: int = 500000  # 500KB
    supported_extensions: list[str] = [".py", ".js", ".java"]

    class Config:
        env_file = ".env"

@lru_cache()
def get_settings():
    return Settings()