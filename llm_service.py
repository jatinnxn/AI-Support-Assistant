import os
from typing import Optional, Type

from dotenv import load_dotenv
from google import genai
from google.genai.types import (
    GenerateContentConfig,
)

load_dotenv()


class LLMService:
    """
    Production-ready Gemini service.
    Supports:
    - Normal text generation
    - Structured (Pydantic) generation
    """

    def __init__(self):

        api_key = os.getenv("GEMINI_API_KEY")
        print("Using API Key:", api_key[:10] + "..." if api_key else "NOT FOUND")

        if not api_key:
            raise ValueError("GEMINI_API_KEY not found.")

        self.client = genai.Client(api_key=api_key)

        self.model = os.getenv(
            "GEMINI_MODEL",
            "gemini-2.5-flash",
        )

    def generate(
        self,
        prompt: str,
        temperature: float = 0.2,
        max_output_tokens: int = 1024,
        system_instruction: Optional[str] = None,
    ) -> str:

        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
            config=GenerateContentConfig(
                temperature=temperature,
                max_output_tokens=max_output_tokens,
                system_instruction=system_instruction,
            ),
        )

        return response.text.strip()

    def generate_structured(
        self,
        prompt: str,
        response_schema: Type,
        system_instruction: Optional[str] = None,
        temperature: float = 0.2,
    ):
        """
        Returns validated Pydantic object directly.
        """

        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
            config=GenerateContentConfig(
                temperature=temperature,
                response_mime_type="application/json",
                response_schema=response_schema,
                system_instruction=system_instruction,
            ),
        )

        return response.parsed


llm_service = LLMService()