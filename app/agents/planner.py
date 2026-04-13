"""
Planner Agent — understands the student's question and produces a learning plan.
Returns a structured plan that all downstream agents follow.
"""

import json
import re
from pathlib import Path

from app.config import MODELS
from app.services.ollama_client import generate
from app.state import PipelineState

_PROMPT_PATH = Path(__file__).parent.parent / "prompts" / "planner.txt"
_PROMPT_TEMPLATE = _PROMPT_PATH.read_text()

# Keywords that reliably signal the student wants a code example.
# Small models miss these in the prompt, so we enforce it in code.
_CODE_TRIGGER_WORDS = [
    "python", "code", "example", "implement", "show me", "demonstrate",
    "snippet", "program", "write a", "give me a",
]


def _student_wants_code(question: str) -> bool:
    q = question.lower()
    return any(kw in q for kw in _CODE_TRIGGER_WORDS)


def _extract_json(raw: str) -> dict:
    """Pull the first JSON object out of raw text, even if surrounded by prose."""
    # Try direct parse first
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        pass

    # Try to extract a JSON block with regex
    match = re.search(r"\{[\s\S]*\}", raw)
    if match:
        try:
            return json.loads(match.group())
        except json.JSONDecodeError:
            pass

    return {}


def run(state: PipelineState) -> PipelineState:
    """
    Call the planner model and populate the planning fields in state.
    All errors are non-fatal: defaults keep the pipeline moving.
    """
    prompt = _PROMPT_TEMPLATE.format(question=state.user_question)

    try:
        raw = generate(
            model=MODELS["planner"],
            prompt=prompt,
            agent_name="planner",
        )
        plan = _extract_json(raw)

        state.topic = plan.get("topic", state.user_question[:60])
        state.question_type = plan.get("question_type", "concept_explanation")
        state.needs_theory = bool(plan.get("needs_theory", True))
        state.needs_example = bool(plan.get("needs_example", True))
        # Always override with keyword detection — small models miss explicit code requests
        state.needs_code = bool(plan.get("needs_code", False)) or _student_wants_code(state.user_question)
        state.needs_review = bool(plan.get("needs_review", True))
        state.learning_steps = plan.get("learning_steps", [])

    except RuntimeError as exc:
        state.errors.append(f"Planner: {exc}")
        # Use safe defaults so the pipeline can continue
        state.topic = state.user_question[:60]
        state.needs_theory = True
        state.needs_example = True
        state.needs_code = _student_wants_code(state.user_question)
        state.needs_review = False

    state.agents_run.append("planner")
    return state
