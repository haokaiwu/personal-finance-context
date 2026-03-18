"""Anthropic (Claude) adapter."""

from typing import Callable, Optional

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
        tools: Optional[list[dict]] = None,
        tool_handler: Optional[Callable[[str, dict], str]] = None,
    ) -> ModelResponse:
        kwargs = {
            "model": self.api_model,
            "max_tokens": 4096,
            "messages": messages,
        }
        if system_prompt is not None:
            kwargs["system"] = system_prompt
        if tools:
            kwargs["tools"] = tools

        total_input = 0
        total_output = 0
        tools_used: list[str] = []

        while True:
            resp = self.client.messages.create(**kwargs)
            total_input += resp.usage.input_tokens
            total_output += resp.usage.output_tokens

            # If no tool use or no handler, return the text response
            if resp.stop_reason != "tool_use" or not tool_handler:
                content = ""
                for block in resp.content:
                    if block.type == "text":
                        content += block.text

                return ModelResponse(
                    content=content,
                    model=self.api_model,
                    input_tokens=total_input,
                    output_tokens=total_output,
                    stop_reason=resp.stop_reason or "",
                    tools_used=tools_used,
                )

            # Handle tool calls: build tool results and loop
            tool_results = []
            for block in resp.content:
                if block.type == "tool_use":
                    tools_used.append(block.input.get("category", block.name))
                    result = tool_handler(block.name, block.input)
                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": result,
                    })

            # Append the assistant's response and tool results to messages
            kwargs["messages"] = list(kwargs["messages"]) + [
                {"role": "assistant", "content": resp.content},
                {"role": "user", "content": tool_results},
            ]
