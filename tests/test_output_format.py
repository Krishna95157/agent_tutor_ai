"""
Tests for the formatter — no Ollama required.
"""

from app.services.formatter import build_final_response
from app.state import PipelineState


def _base_state() -> PipelineState:
    return PipelineState(
        user_question="What is overfitting?",
        topic="overfitting",
        learning_steps=["Define overfitting", "Explain cause", "Give analogy"],
        theory_text="Overfitting happens when a model learns training data too closely.",
    )


def test_formatter_returns_string():
    state = _base_state()
    result = build_final_response(state)
    assert isinstance(result, str)
    assert len(result) > 0


def test_formatter_includes_theory():
    state = _base_state()
    result = build_final_response(state)
    assert "Overfitting happens" in result


def test_formatter_skips_code_when_absent():
    state = _base_state()
    state.code_snippet = None
    result = build_final_response(state)
    assert "```python" not in result


def test_formatter_includes_code_when_present():
    state = _base_state()
    state.code_snippet = "x = 1  # example"
    state.code_purpose = "Illustrate the concept"
    result = build_final_response(state)
    assert "```python" in result
    assert "x = 1" in result


def test_formatter_shows_revised_theory_over_original():
    state = _base_state()
    state.revision_needed = True
    state.revised_theory = "This is the improved explanation."
    result = build_final_response(state)
    assert "improved explanation" in result


def test_formatter_includes_missing_points():
    state = _base_state()
    state.missing_points = ["Consider regularisation", "Mention cross-validation"]
    result = build_final_response(state)
    assert "regularisation" in result


def test_formatter_includes_takeaway():
    state = _base_state()
    result = build_final_response(state)
    assert "overfitting" in result.lower()
