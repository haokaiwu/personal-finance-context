"""Configuration loaded from environment variables."""

import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# Google Sheets
GOOGLE_SERVICE_ACCOUNT_FILE = os.getenv("GOOGLE_SERVICE_ACCOUNT_FILE", "service-account.json")
GOOGLE_SHEET_NAME = os.getenv("GOOGLE_SHEET_NAME", "WorthiQ Test Harness")

# API Keys
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")

# Methodology
METHODOLOGY_DIR = Path(os.getenv("METHODOLOGY_DIR", "../methodology"))

# Model defaults
DEFAULT_MODEL = "claude-sonnet-4-5"

MODEL_REGISTRY = {
    # Anthropic
    "claude-sonnet-4-5": {"provider": "anthropic", "api_model": "claude-sonnet-4-5-20250514"},
    "claude-haiku-4-5": {"provider": "anthropic", "api_model": "claude-haiku-4-5-20250414"},
    "claude-opus-4": {"provider": "anthropic", "api_model": "claude-opus-4-20250514"},
    # OpenAI
    "gpt-4o": {"provider": "openai", "api_model": "gpt-4o"},
    "gpt-4o-mini": {"provider": "openai", "api_model": "gpt-4o-mini"},
    "o3-mini": {"provider": "openai", "api_model": "o3-mini"},
    # Google
    "gemini-2.0-flash": {"provider": "google", "api_model": "gemini-2.0-flash"},
    "gemini-2.5-pro": {"provider": "google", "api_model": "gemini-2.5-pro-preview-06-05"},
}

# Session limits
MAX_TURNS = 20
