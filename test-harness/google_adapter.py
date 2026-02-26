"""Google (Gemini) adapter using the google-genai SDK."""

from typing import Optional

from google import genai
from google.genai import types

from config import GOOGLE_API_KEY
from models.base import BaseAdapter, ModelResponse


class GoogleAdapter(BaseAdapter):
    def __init__(self, api_model: str):
        self.api_model = api_model
        self.client = genai.Client(api_key=GOOGLE_API_KEY)

    def send(
        self,
        messages: list[dict],
        system_prompt: Optional[str] = None,
    ) -> ModelResponse:
        # Convert messages to Gemini content format
        contents = []
        for msg in messages:
            role = "user" if msg["role"] == "user" else "model"
            contents.append(
                types.Content(
                    role=role,
                    parts=[types.Part(text=msg["content"])],
                )
            )

        config = types.GenerateContentConfig(
            max_output_tokens=4096,
        )
        if system_prompt is not None:
            config.system_instruction = system_prompt

        resp = self.client.models.generate_content(
            model=self.api_model,
            contents=contents,
            config=config,
        )

        content = resp.text or ""
        usage = resp.usage_metadata

        return ModelResponse(
            content=content,
            model=self.api_model,
            input_tokens=usage.prompt_token_count if usage else 0,
            output_tokens=usage.candidates_token_count if usage else 0,
            stop_reason=resp.candidates[0].finish_reason.name if resp.candidates else "",
        )
