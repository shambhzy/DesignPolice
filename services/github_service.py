import aiohttp
from typing import List, Dict
import base64
from config import Settings

class GitHubAdapter:
    def __init__(self, settings: Settings):
        self.token = settings.github_token
        self.repo = settings.github_repo
        self.base_url = settings.github_base_url
        self.headers = {
            "Authorization": f"token {self.token}",
            "Accept": "application/vnd.github.v3+json"
        }
    
    async def get_file_content(self, file_path: str) -> str:
        async with aiohttp.ClientSession() as session:
            url = f"{self.base_url}/repos/{self.repo}/contents/{file_path}"
            async with session.get(url, headers=self.headers) as response:
                if response.status == 200:
                    file_data = await response.json()
                    return base64.b64decode(file_data["content"]).decode("utf-8")
                raise Exception(f"Failed to get file content: {await response.text()}")


    async def get_repository_files(self, path: str = "") -> List[Dict]:
        async with aiohttp.ClientSession() as session:
            url = f"{self.base_url}/repos/{self.repo}/contents/{path}"
            async with session.get(url, headers=self.headers) as response:
                if response.status == 200:
                    return await response.json()
                raise Exception(f"Failed to get repository files: {await response.text()}")

    async def create_pull_request(self, branch_name: str, file_path: str, 
                                new_code: str, title: str, description: str) -> Dict:
        # Implementation of creating a PR
        # This would involve:
        # 1. Creating a new branch
        # 2. Committing changes
        # 3. Creating the PR
        pass

