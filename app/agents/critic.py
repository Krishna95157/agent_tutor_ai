"""
Critic Agent — reviews the full answer and improves it if needed.
Only called when the planner sets needs_review = True.
"""

import json
import re
from pathlib import Path

from app.config import MODELS
from app.services.ollama_client import generate
from app.state import PipelineState

_PROMPT_PATH = Path(__file__).parent.parent / "prompts" / "critic.txt"
_PROMPT_TEMPLATE = _PROMPT_PATH.read_text()

# ── Editorial detection ───────────────────────────────────────────
# Any item whose first word is one of these is an instruction to the author,
# not a fact for the student. We strip these from missing_points entirely.
_EDITORIAL_FIRST_WORDS = {
    "explain", "clarify", "add", "include", "describe", "mention",
    "show", "provide", "expand", "cover", "discuss", "elaborate",
    "give", "write", "create", "list", "define", "address",
    "consider", "note", "highlight", "illustrate", "demonstrate",
    "introduce", "present", "specify", "detail", "outline",
    "compare", "contrast", "state", "make", "ensure", "try",
}

# Phrase patterns anywhere in the string that also mark editorial content
_EDITORIAL_PATTERNS = re.compile(
    r"\b(should (include|explain|mention|cover|add|address|provide|clarify|show)|"
    r"needs? to (explain|include|mention|cover|clarify|address)|"
    r"would benefit from|could (add|include|mention|explain)|"
    r"it (would|might) (help|be helpful))\b",
    re.IGNORECASE,
)


def _is_editorial(text: str) -> bool:
    """
    Return True if the string looks like an editorial instruction
    rather than a student-facing fact.
    Two checks:
      1. First word is a known imperative/instruction verb.
      2. The sentence contains a common editorial phrase pattern.
    """
    stripped = text.strip()
    if not stripped:
        return True
    first_word = stripped.lower().split()[0].rstrip(".,:")
    if first_word in _EDITORIAL_FIRST_WORDS:
        return True
    if _EDITORIAL_PATTERNS.search(stripped):
        return True
    return False


def _extract_json(raw: str) -> dict:
    """Pull the first JSON object out of raw text."""
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        pass
    match = re.search(r"\{[\s\S]*\}", raw)
    if match:
        try:
            return json.loads(match.group())
        except json.JSONDecodeError:
            pass
    return {}


def _build_key_points(raw_key: list, raw_missing: list, topic: str) -> list:
    """
    Return the final key_points list.
    Priority:
      1. Use raw_key if the model provided non-editorial items.
      2. Promote factual items from raw_missing.
      3. Fall back to safe generic warnings about the topic.
    """
    # Filter editorial items from whatever the model returned
    clean_key = [pt for pt in raw_key if not _is_editorial(pt)]
    if clean_key:
        return clean_key[:3]

    # Promote factual missing_points to key_points
    factual_missing = [pt for pt in raw_missing if not _is_editorial(pt)]
    if factual_missing:
        return factual_missing[:3]

    # Generic fallback — section 6 is never blank
    return [
        f"Make sure you understand the core definition of {topic} before applying it.",
        f"A common mistake is confusing {topic} with a related but different concept.",
        f"Always verify your assumptions and data before using {topic} in practice.",
    ]


def run(state: PipelineState) -> PipelineState:
    """
    Review the explanation (and code if present) and update state with critic feedback.
    Skipped automatically if state.needs_review is False.
    """
    if not state.needs_review:
        state.agents_run.append("critic (skipped)")
        return state

    prompt = _PROMPT_TEMPLATE.format(
        question=state.user_question,
        topic=state.topic,
        theory=state.theory_text[:800],
        code=state.code_snippet or "(none)",
    )

    try:
        raw = generate(
            model=MODELS["critic"],
            prompt=prompt,
            agent_name="critic",
        )
        feedback = _extract_json(raw)

        state.clarity_check = feedback.get("clarity_check", "good")
        state.code_feedback = feedback.get("code_feedback", "n/a")
        state.revision_needed = bool(feedback.get("revision_needed", False))

        raw_missing = feedback.get("missing_points", [])
        raw_key = feedback.get("key_points", [])

        # missing_points: only factual items shown to students (editorial ones stripped)
        state.missing_points = [pt for pt in raw_missing if not _is_editorial(pt)]

        # key_points: always has content — model output, promoted facts, or generic fallback
        state.key_points = _build_key_points(raw_key, raw_missing, state.topic)

        revised = feedback.get("revised_theory")
        if state.revision_needed and revised and revised.lower() != "null":
            state.revised_theory = revised

    except RuntimeError as exc:
        state.errors.append(f"Critic: {exc}")
        # Guarantee key_points is never empty even on error
        if not state.key_points:
            state.key_points = _build_key_points([], [], state.topic)

    state.agents_run.append("critic")
    return state
