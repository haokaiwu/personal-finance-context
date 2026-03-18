"""Model factory — resolves a friendly model name to the right adapter."""

from config import MODEL_REGISTRY
from models.base import BaseAdapter
from models.anthropic_adapter import AnthropicAdapter
from models.openai_adapter import OpenAIAdapter
from models.google_adapter import GoogleAdapter

_PROVIDERS = {
    "anthropic": AnthropicAdapter,
    "openai": OpenAIAdapter,
    "google": GoogleAdapter,
}


def get_adapter(model_name: str) -> BaseAdapter:
    """Return an adapter instance for the given friendly model name."""
    if model_name not in MODEL_REGISTRY:
        available = ", ".join(sorted(MODEL_REGISTRY.keys()))
        raise ValueError(f"Unknown model '{model_name}'. Available: {available}")

    entry = MODEL_REGISTRY[model_name]
    adapter_cls = _PROVIDERS[entry["provider"]]
    return adapter_cls(api_model=entry["api_model"])


def list_models() -> list[str]:
    return sorted(MODEL_REGISTRY.keys())
