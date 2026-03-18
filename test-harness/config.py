"""Configuration loaded from environment variables."""

import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# Google Sheets
GOOGLE_SERVICE_ACCOUNT_FILE = os.getenv("GOOGLE_SERVICE_ACCOUNT_FILE", "service-account.json")
GOOGLE_SHEET_NAME = os.getenv("GOOGLE_SHEET_NAME", "WorthiQ Test Harness")
GOOGLE_SHEET_KEY = os.getenv("GOOGLE_SHEET_KEY", "")

# API Keys
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")

# Methodology
METHODOLOGY_DIR = Path(os.getenv("METHODOLOGY_DIR", "../methodology"))
VALID_MODES = ("without", "general", "category", "category-all")

# Model defaults
DEFAULT_MODEL = "claude-sonnet-4-6"

MODEL_REGISTRY = {
    # Anthropic
    "claude-sonnet-4-6": {"provider": "anthropic", "api_model": "claude-sonnet-4-6"},
    "claude-haiku-4-5": {"provider": "anthropic", "api_model": "claude-haiku-4-5"},
    "claude-opus-4-6": {"provider": "anthropic", "api_model": "claude-opus-4-6"},
    # OpenAI
    "gpt-5.4": {"provider": "openai", "api_model": "gpt-5.4"},
    "gpt-5.4-mini": {"provider": "openai", "api_model": "gpt-5.4-mini"},
    "gpt-5.4-nano": {"provider": "openai", "api_model": "gpt-5.4-nano"},
    # Google
    "gemini-3-flash-preview": {"provider": "google", "api_model": "gemini-3-flash-preview"},
    "gemini-3.1-pro-preview": {"provider": "google", "api_model": "gemini-3.1-pro-preview"},
}

# Session limits
MAX_TURNS = 20
