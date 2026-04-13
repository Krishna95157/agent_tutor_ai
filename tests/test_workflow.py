"""
Integration-style tests for the full pipeline — mocks Ollama.
"""

from unittest.mock import patch

from app.workflow import run_pipeline, stream_pipeline

PLANNER_OUT = '{"topic":"overfitting","question_type":"concept_explanation","needs_theory":true,"needs_example":true,"needs_code":false,"needs_review":false,"learning_steps":["Define overfitting","Explain cause","Give analogy"]}'
EXPLAINER_OUT = "Overfitting occurs when a model learns the training data too well, including noise."
CRITIC_OUT = '{"clarity_check":"good","missing_points":[],"code_feedback":"n/a","revision_needed":false,"revised_theory":null}'


@patch("app.agents.critic.generate", return_value=CRITIC_OUT)
@patch("app.agents.explainer.generate", return_value=EXPLAINER_OUT)
@patch("app.agents.planner.generate", return_value=PLANNER_OUT)
def test_pipeline_returns_string(mock_plan, mock_exp, mock_crit):
    result, state = run_pipeline("What is overfitting?")
    assert isinstance(result, str)
    assert len(result) > 10
    assert "overfitting" in result.lower()


@patch("app.agents.critic.generate", return_value=CRITIC_OUT)
@patch("app.agents.explainer.generate", return_value=EXPLAINER_OUT)
@patch("app.agents.planner.generate", return_value=PLANNER_OUT)
def test_pipeline_agents_run_recorded(mock_plan, mock_exp, mock_crit):
    _, state = run_pipeline("What is overfitting?")
    assert "planner" in state.agents_run
    assert "explainer" in state.agents_run


def test_pipeline_rejects_off_topic():
    result, state = run_pipeline("What is the capital of France?")
    assert "only" in result.lower() or "focuses" in result.lower() or "covers" in result.lower()


@patch("app.agents.critic.generate", return_value=CRITIC_OUT)
@patch("app.agents.explainer.generate", return_value=EXPLAINER_OUT)
@patch("app.agents.planner.generate", return_value=PLANNER_OUT)
def test_stream_pipeline_yields_events(mock_plan, mock_exp, mock_crit):
    events = list(stream_pipeline("What is overfitting?"))
    event_types = [e[0] for e in events]
    assert "agent_start" in event_types
    assert "agent_done" in event_types
    assert "result" in event_types


@patch("app.agents.critic.generate", return_value=CRITIC_OUT)
@patch("app.agents.explainer.generate", return_value=EXPLAINER_OUT)
@patch("app.agents.planner.generate", return_value=PLANNER_OUT)
def test_pipeline_callbacks_called(mock_plan, mock_exp, mock_crit):
    started = []
    finished = []
    run_pipeline(
        "What is overfitting?",
        on_agent_start=lambda n: started.append(n),
        on_agent_done=lambda n: finished.append(n),
    )
    assert len(started) == 4
    assert len(finished) == 4
