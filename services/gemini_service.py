import asyncio
import json
import google.generativeai as genai
from typing import Dict, List, Union
from tenacity import retry, wait_exponential, stop_after_attempt

class GeminiAdapter:
    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel("gemini-pro")
        self.max_tokens = 30720  # Gemini's token limit

    def _split_prompt(self, prompt: str) -> List[str]:
        """Splits the prompt into smaller chunks if it exceeds the token limit."""
        if len(prompt) <= self.max_tokens:
            return [prompt]

        chunks = []
        words = prompt.split()
        chunk = []

        for word in words:
            chunk.append(word)
            if len(" ".join(chunk)) > self.max_tokens - 1000:  # Keep some buffer
                chunks.append(" ".join(chunk))
                chunk = []

        if chunk:
            chunks.append(" ".join(chunk))

        return chunks

    @retry(wait=wait_exponential(multiplier=1, min=2, max=10), stop=stop_after_attempt(5))
    async def analyze_code(self, prompt: str) -> Union[List[Dict], str]:
        try:
            loop = asyncio.get_event_loop()
            results = []

            for chunk in self._split_prompt(prompt):
                response = await loop.run_in_executor(None, self.model.generate_content, chunk)

                # Extract text properly
                if response and hasattr(response, "parts") and response.parts:
                    text_response = response.parts[0].text.strip()
                else:
                    print("Error: Gemini API response did not contain expected 'parts'.")
                    return "Error: Unexpected response format"

                # Check for quota errors
                if "quota" in text_response.lower() or "429" in text_response:
                    print("Error: Gemini API quota exceeded. Consider upgrading the plan.")
                    return "Error: Quota exceeded"

                # ✅ If the response starts with `[`, it's already valid JSON
                if text_response.startswith("["):
                    results.extend(json.loads(text_response))
                else:
                    print(f"Error: Unexpected non-JSON response:\n{text_response}")
                    return "Error: Unexpected response"

            return results
        except Exception as e:
            print(f"Error in Gemini analysis: {str(e)}")
            return f"Error: {str(e)}"
