"""Anthropic (Claude) adapter."""

from typing import Optional

import anthropic

from config import ANTHROPIC_API_KEY
from models.base import BaseAdapter, ModelResponse


class AnthropicAdapter(BaseAdapter):
    def __init__(self, api_model: str):
        self.api_model = api_model
        self.client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

    def send(
        self,
        messages: list[dict],
        system_prompt: Optional[str] = None,
    ) -> ModelResponse:
        kwargs = {
            "model": self.api_model,
            "max_tokens": 4096,
            "messages": messages,
        }
        if system_prompt is not None:
            kwargs["system"] = system_prompt

        resp = self.client.messages.create(**kwargs)

        content = ""
        for block in resp.content:
            if block.type == "text":
                content += block.text

        return ModelResponse(
            content=content,
            model=self.api_model,
            input_tokens=resp.usage.input_tokens,
            output_tokens=resp.usage.output_tokens,
            stop_reason=resp.stop_reason or "",
        )
