"""OpenAI (GPT / o-series) adapter."""

from typing import Optional

from openai import OpenAI

from config import OPENAI_API_KEY
from models.base import BaseAdapter, ModelResponse


class OpenAIAdapter(BaseAdapter):
    def __init__(self, api_model: str):
        self.api_model = api_model
        self.client = OpenAI(api_key=OPENAI_API_KEY)

    def send(
        self,
        messages: list[dict],
        system_prompt: Optional[str] = None,
    ) -> ModelResponse:
        api_messages = []
        if system_prompt is not None:
            api_messages.append({"role": "system", "content": system_prompt})
        api_messages.extend(messages)

        resp = self.client.chat.completions.create(
            model=self.api_model,
            messages=api_messages,
            max_completion_tokens=4096,
        )

        choice = resp.choices[0]
        usage = resp.usage

        return ModelResponse(
            content=choice.message.content or "",
            model=self.api_model,
            input_tokens=usage.prompt_tokens if usage else 0,
            output_tokens=usage.completion_tokens if usage else 0,
            stop_reason=choice.finish_reason or "",
        )
