"""Base class for model adapters."""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional


@dataclass
class ModelResponse:
    """Standardized response from any model."""
    content: str
    model: str
    input_tokens: int = 0
    output_tokens: int = 0
    stop_reason: str = ""


class BaseAdapter(ABC):
    """Interface every model adapter must implement."""

    @abstractmethod
    def send(
        self,
        messages: list[dict],
        system_prompt: Optional[str] = None,
    ) -> ModelResponse:
        """Send a conversation and return the assistant's response.

        Args:
            messages: list of {"role": "user"|"assistant", "content": "..."}
            system_prompt: optional system-level instructions.
                           None = use model's default (control condition).
        """
        ...
