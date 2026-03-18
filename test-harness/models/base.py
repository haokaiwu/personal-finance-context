"""Base class for model adapters."""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Callable, Optional


@dataclass
class ModelResponse:
    """Standardized response from any model."""
    content: str
    model: str
    input_tokens: int = 0
    output_tokens: int = 0
    stop_reason: str = ""
    tools_used: list[str] = field(default_factory=list)


class BaseAdapter(ABC):
    """Interface every model adapter must implement."""

    @abstractmethod
    def send(
        self,
        messages: list[dict],
        system_prompt: Optional[str] = None,
        tools: Optional[list[dict]] = None,
        tool_handler: Optional[Callable[[str, dict], str]] = None,
    ) -> ModelResponse:
        """Send a conversation and return the assistant's response.

        Args:
            messages: list of {"role": "user"|"assistant", "content": "..."}
            system_prompt: optional system-level instructions.
                           None = use model's default (control condition).
            tools: optional tool definitions (provider-specific format).
            tool_handler: callback(tool_name, tool_input) -> result string.
                          Called when the model invokes a tool; the adapter
                          loops until the model produces a final text response.
        """
        ...
