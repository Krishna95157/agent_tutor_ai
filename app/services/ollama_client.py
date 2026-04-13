"""
Thin wrapper around the Ollama /api/generate endpoint.
Keeps networking logic in one place so agents stay clean.
"""

import json
import requests
from app.config import OLLAMA_BASE_URL, MAX_TOKENS, _FALLBACKS


def _resolve_model(model: str) -> str:
    """Return fallback model name if the preferred model isn't pulled yet."""
    if not is_model_available(model):
        fallback = _FALLBACKS.get(model)
        if fallback and is_model_available(fallback):
            return fallback
    return model


def generate(model: str, prompt: str, agent_name: str) -> str:
    """
    Call Ollama and return the full response text.
    agent_name is used only to look up the token cap.
    Raises RuntimeError if the server is unreachable.
    """
    model = _resolve_model(model)
    url = f"{OLLAMA_BASE_URL}/api/generate"
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False,
        "options": {
            "num_predict": MAX_TOKENS.get(agent_name, 400),
            "temperature": 0.3,
            "top_p": 0.9,
        },
    }

    try:
        response = requests.post(url, json=payload, timeout=120)
        response.raise_for_status()
        data = response.json()
        return data.get("response", "").strip()
    except requests.exceptions.ConnectionError:
        raise RuntimeError(
            "Cannot reach Ollama. Make sure Ollama is running: open the Ollama app "
            "or run 'ollama serve' in a terminal."
        )
    except requests.exceptions.Timeout:
        raise RuntimeError("Ollama request timed out. The model may be too slow — try a smaller one.")
    except Exception as exc:
        raise RuntimeError(f"Ollama error: {exc}")


def is_model_available(model: str) -> bool:
    """Return True if the model is already pulled."""
    try:
        resp = requests.get(f"{OLLAMA_BASE_URL}/api/tags", timeout=10)
        resp.raise_for_status()
        names = [m["name"] for m in resp.json().get("models", [])]
        # match with or without the :latest suffix
        return any(model in n or n in model for n in names)
    except Exception:
        return False


def list_models() -> list:
    """Return a list of pulled model names."""
    try:
        resp = requests.get(f"{OLLAMA_BASE_URL}/api/tags", timeout=10)
        resp.raise_for_status()
        return [m["name"] for m in resp.json().get("models", [])]
    except Exception:
        return []
