"""
Sequential pipeline orchestrator.
Runs agents one at a time to keep RAM usage low on MacBook Air M1.

Pipeline:
  User Question → Planner → Explainer → Developer (optional) → Critic (optional) → Final Response
"""

from typing import Callable, Generator, Optional

from app.agents import critic, developer, explainer, planner
from app.services.formatter import build_final_response
from app.state import PipelineState
from app.utils.validators import is_in_scope


def run_pipeline(
    question: str,
    on_agent_start: Optional[Callable[[str], None]] = None,
    on_agent_done: Optional[Callable[[str], None]] = None,
) -> tuple[str, PipelineState]:
    """
    Run the full multi-agent pipeline for a student question.

    Args:
        question: The student's raw question string.
        on_agent_start: Optional callback called with agent name when it begins.
        on_agent_done:  Optional callback called with agent name when it finishes.

    Returns:
        (final_response_markdown, final_state)
    """
    state = PipelineState(user_question=question.strip())

    # Domain guard — reject off-topic questions early
    if not is_in_scope(question):
        state.theory_text = (
            "This system focuses on Artificial Intelligence, Machine Learning, "
            "Deep Learning, and Data Mining topics only. "
            "Please ask a question within those areas."
        )
        state.agents_run.append("router (blocked)")
        return build_final_response(state), state

    def _run_agent(name: str, fn: Callable[[PipelineState], PipelineState]) -> None:
        if on_agent_start:
            on_agent_start(name)
        fn(state)
        if on_agent_done:
            on_agent_done(name)

    # Sequential execution — one agent at a time
    _run_agent("Planner", planner.run)
    _run_agent("Explainer", explainer.run)
    _run_agent("Developer", developer.run)
    _run_agent("Critic", critic.run)

    return build_final_response(state), state


def stream_pipeline(question: str) -> Generator[tuple, None, None]:
    """
    Generator version for Streamlit live updates.

    Yields (event_type, payload) tuples:
      ("agent_start", agent_name)
      ("agent_done",  agent_name)
      ("result",      final_markdown)
      ("error",       error_message)
    """
    state = PipelineState(user_question=question.strip())

    if not is_in_scope(question):
        yield "result", (
            "This system covers Artificial Intelligence, Machine Learning, "
            "Deep Learning, and Data Mining only. Please ask a question in those areas."
        )
        return

    steps = [
        ("Planner Agent", planner.run),
        ("Explainer Agent", explainer.run),
        ("Developer Agent", developer.run),
        ("Critic Agent", critic.run),
    ]

    for agent_label, fn in steps:
        yield "agent_start", agent_label
        try:
            fn(state)
        except Exception as exc:
            state.errors.append(str(exc))
            yield "error", f"{agent_label} failed: {exc}"
        yield "agent_done", agent_label

    final = build_final_response(state)
    yield "result", final
