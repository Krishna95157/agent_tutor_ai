"""
Input validation helpers.
"""

from app.config import ALLOWED_DOMAINS


def is_in_scope(question: str) -> bool:
    """
    Return True if the question likely belongs to the AI/ML/DL/Data Mining domain.
    Uses a simple keyword match against ALLOWED_DOMAINS from config.
    """
    q_lower = question.lower()
    return any(keyword in q_lower for keyword in ALLOWED_DOMAINS)


def sanitise_question(question: str) -> str:
    """Strip leading/trailing whitespace and cap length to avoid prompt injection abuse."""
    return question.strip()[:500]
