"""
Unit tests for agent logic — mocks Ollama so no model needs to run.
"""

from unittest.mock import patch

from app.agents import critic, developer, explainer, planner
from app.state import PipelineState


def _state(question="What is gradient descent?") -> PipelineState:
    return PipelineState(user_question=question)


# ── Planner ───────────────────────────────────────────────────────────────────

PLANNER_JSON = """{
  "topic": "gradient descent",
  "question_type": "concept_explanation",
  "needs_theory": true,
  "needs_example": true,
  "needs_code": false,
  "needs_review": true,
  "learning_steps": ["Define gradient descent", "Give intuition", "Give analogy"]
}"""


@patch("app.agents.planner.generate", return_value=PLANNER_JSON)
def test_planner_parses_json(mock_gen):
    state = _state()
    planner.run(state)
    assert state.topic == "gradient descent"
    assert state.question_type == "concept_explanation"
    assert state.needs_code is False
    assert len(state.learning_steps) == 3
    assert "planner" in state.agents_run


@patch("app.agents.planner.generate", side_effect=RuntimeError("Ollama down"))
def test_planner_graceful_on_error(mock_gen):
    state = _state()
    planner.run(state)
    assert len(state.errors) == 1
    assert "planner" in state.agents_run
    # Safe defaults applied
    assert state.needs_theory is True


@patch("app.agents.planner.generate", return_value="Some prose before { bad json }")
def test_planner_handles_bad_json(mock_gen):
    state = _state()
    planner.run(state)
    # Should not raise; topic falls back to question prefix
    assert "planner" in state.agents_run


# ── Explainer ─────────────────────────────────────────────────────────────────

@patch("app.agents.explainer.generate", return_value="Gradient descent is an optimisation algorithm.")
def test_explainer_stores_theory(mock_gen):
    state = _state()
    state.topic = "gradient descent"
    state.learning_steps = ["Define", "Explain intuition"]
    explainer.run(state)
    assert "optimisation" in state.theory_text
    assert "explainer" in state.agents_run


@patch("app.agents.explainer.generate", side_effect=RuntimeError("timeout"))
def test_explainer_graceful_on_error(mock_gen):
    state = _state()
    explainer.run(state)
    assert "explainer" in state.agents_run
    assert "Could not generate" in state.theory_text


# ── Developer ─────────────────────────────────────────────────────────────────

@patch("app.agents.developer.generate", return_value="learning_rate = 0.01\n# update step")
def test_developer_runs_when_needed(mock_gen):
    state = _state()
    state.topic = "gradient descent"
    state.needs_code = True
    state.theory_text = "Gradient descent minimises a loss function."
    developer.run(state)
    assert state.code_snippet is not None
    assert "developer" in state.agents_run


def test_developer_skipped_when_not_needed():
    state = _state()
    state.needs_code = False
    developer.run(state)
    assert state.code_snippet is None
    assert any("skipped" in a for a in state.agents_run)


@patch("app.agents.developer.generate", return_value="```python\nx = 1\n```")
def test_developer_strips_markdown_fences(mock_gen):
    state = _state()
    state.needs_code = True
    state.topic = "test"
    state.theory_text = "some theory"
    developer.run(state)
    assert state.code_snippet is not None
    assert "```" not in state.code_snippet


# ── Critic ────────────────────────────────────────────────────────────────────

CRITIC_JSON = """{
  "clarity_check": "good",
  "missing_points": ["Mention learning rate"],
  "code_feedback": "n/a",
  "revision_needed": false,
  "revised_theory": null
}"""


@patch("app.agents.critic.generate", return_value=CRITIC_JSON)
def test_critic_parses_feedback(mock_gen):
    state = _state()
    state.topic = "gradient descent"
    state.theory_text = "Gradient descent is an optimisation algorithm."
    state.needs_review = True
    critic.run(state)
    assert state.clarity_check == "good"
    assert "Mention learning rate" in state.missing_points
    assert state.revision_needed is False
    assert "critic" in state.agents_run


@patch("app.agents.critic.generate", return_value='{"clarity_check":"needs_improvement","missing_points":[],"code_feedback":"n/a","revision_needed":true,"revised_theory":"Better explanation here."}')
def test_critic_stores_revised_theory(mock_gen):
    state = _state()
    state.topic = "test"
    state.theory_text = "Short."
    state.needs_review = True
    critic.run(state)
    assert state.revision_needed is True
    assert state.revised_theory == "Better explanation here."


def test_critic_skipped_when_not_needed():
    state = _state()
    state.needs_review = False
    critic.run(state)
    assert any("skipped" in a for a in state.agents_run)
