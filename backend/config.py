import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")


def get_setting(name: str, default: str = "") -> str:
    # Streamlit Cloud Secrets
    try:
        import streamlit as st

        value = st.secrets.get(name)

        if value is not None:
            return str(value).strip()
    except Exception:
        pass

    # Local .env / environment variables
    return os.getenv(name, default).strip()


GEMINI_API_KEY = get_setting("GEMINI_API_KEY")
GEMINI_MODEL = get_setting(
    "GEMINI_MODEL",
    "gemini-3.5-flash-lite",
)

MOCK_AI = get_setting(
    "MOCK_AI",
    "false",
).lower() in {"1", "true", "yes", "on"}

BACKEND_URL = get_setting(
    "BACKEND_URL",
    "http://127.0.0.1:8000",
).rstrip("/")


_raw_origins = get_setting(
    "CORS_ORIGINS",
    "http://localhost:8501,http://127.0.0.1:8501",
)

CORS_ORIGINS = [
    item.strip()
    for item in _raw_origins.split(",")
    if item.strip()
]