"""
Developer Agent — writes a short, beginner-friendly Python code example
and a step-by-step explanation of that code.
Only called when the planner sets needs_code = True.
"""

from pathlib import Path
from typing import Tuple

from app.config import MODELS
from app.services.ollama_client import generate
from app.state import PipelineState

_PROMPT_PATH = Path(__file__).parent.parent / "prompts" / "developer.txt"
_PROMPT_TEMPLATE = _PROMPT_PATH.read_text()


def _clean_code(raw: str) -> str:
    """Strip markdown code fences if the model included them."""
    lines = raw.strip().splitlines()
    if lines and lines[0].strip().startswith("```"):
        lines = lines[1:]
    if lines and lines[-1].strip() == "```":
        lines = lines[:-1]
    return "\n".join(lines).strip()


def _parse_code_and_explanation(raw: str) -> Tuple[str, str]:
    """
    Parse CODE: and EXPLANATION: sections from model output.
    Falls back to treating the entire output as code if no labels found.
    """
    code = ""
    explanation = ""

    lines = raw.strip().splitlines()
    current = None
    buffer = []

    for line in lines:
        upper = line.strip().upper()
        if upper.startswith("CODE:") or upper == "CODE":
            if current == "explanation":
                explanation = "\n".join(buffer).strip()
            current = "code"
            buffer = []
        elif upper.startswith("EXPLANATION:") or upper == "EXPLANATION":
            if current == "code":
                code = "\n".join(buffer).strip()
            current = "explanation"
            buffer = []
        elif current:
            buffer.append(line)

    # Flush last section
    if buffer:
        if current == "code":
            code = "\n".join(buffer).strip()
        elif current == "explanation":
            explanation = "\n".join(buffer).strip()

    # Fallback: if no CODE: label found, treat entire output as code
    if not code:
        code = _clean_code(raw)

    return _clean_code(code), explanation


def run(state: PipelineState) -> PipelineState:
    """
    Generate a code snippet + explanation and store in state.
    Skipped automatically if state.needs_code is False.
    """
    if not state.needs_code:
        state.agents_run.append("developer (skipped)")
        return state

    # Build the theory text to pass into the prompt — use revised_theory if available
    theory_for_prompt = state.revised_theory or state.theory_text or ""

    prompt = _PROMPT_TEMPLATE.format(
        question=state.user_question,
        topic=state.topic,
        theory=theory_for_prompt[:800],   # cap to keep prompt short
    )

    try:
        raw = generate(
            model=MODELS["developer"],
            prompt=prompt,
            agent_name="developer",
        )
        code, explanation = _parse_code_and_explanation(raw)
        state.code_snippet = code
        state.code_explanation = explanation
        state.code_purpose = f"Simple Python illustration of {state.topic}"
    except RuntimeError as exc:
        state.errors.append(f"Developer: {exc}")
        state.code_snippet = None
        state.code_explanation = ""

    state.agents_run.append("developer")
    return state
