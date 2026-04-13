"""
Router — decides whether the question should enter the pipeline.
Thin layer that wraps the validator so workflow.py stays clean.
"""

from app.utils.validators import is_in_scope


def can_answer(question: str) -> bool:
    """Return True if the question is within the allowed AI/ML/DL/DM domain."""
    return is_in_scope(question)


def rejection_message() -> str:
    return (
        "Sorry, this assistant only covers **Artificial Intelligence**, "
        "**Machine Learning**, **Deep Learning**, and **Data Mining** topics. "
        "Please ask a question within those areas."
    )
