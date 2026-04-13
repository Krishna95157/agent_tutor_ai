"""
Explainer Agent — the core teacher.
Writes a clear, beginner-friendly theory explanation split into three sections:
  1. Simple Explanation
  2. Why It Matters
  3. Intuition and Example
"""

from pathlib import Path
from typing import Tuple

from app.config import MODELS
from app.services.ollama_client import generate
from app.state import PipelineState

_PROMPT_PATH = Path(__file__).parent.parent / "prompts" / "explainer.txt"
_PROMPT_TEMPLATE = _PROMPT_PATH.read_text()

# Labels the model is asked to use — ordered so we scan in sequence
_SECTION_LABELS = [
    ("simple",    ["SIMPLE EXPLANATION", "SIMPLE:"]),
    ("why",       ["WHY IT MATTERS", "WHY THIS MATTERS", "WHY:"]),
    ("intuition", ["INTUITION AND EXAMPLE", "INTUITION:", "EXAMPLE:", "ANALOGY:"]),
]


def _parse_sections(raw: str) -> Tuple[str, str, str]:
    """
    Parse the three labeled sections from the model's response.
    Falls back gracefully: if the model didn't use labels, the full
    text becomes the Simple Explanation.
    """
    simple = ""
    why = ""
    intuition = ""

    lines = raw.strip().splitlines()
    current = None
    buffer = []

    def flush(section_name, buf):
        text = "\n".join(buf).strip()
        return text if text else ""

    for line in lines:
        upper = line.strip().upper().rstrip(":")

        matched = None
        for key, variants in _SECTION_LABELS:
            if any(upper == v or upper.startswith(v) for v in variants):
                matched = key
                break

        if matched:
            # Save previous buffer
            if current == "simple":
                simple = flush("simple", buffer)
            elif current == "why":
                why = flush("why", buffer)
            elif current == "intuition":
                intuition = flush("intuition", buffer)
            current = matched
            buffer = []
        elif current:
            buffer.append(line)

    # Flush last section
    if buffer:
        if current == "simple":
            simple = flush("simple", buffer)
        elif current == "why":
            why = flush("why", buffer)
        elif current == "intuition":
            intuition = flush("intuition", buffer)

    # Fallback: if parsing found nothing, use full text as simple explanation
    if not simple:
        simple = raw.strip()

    return simple, why, intuition


def run(state: PipelineState) -> PipelineState:
    """Generate the theory explanation (3 sections) and store in state."""
    steps_text = (
        "\n".join(f"- {s}" for s in state.learning_steps)
        if state.learning_steps
        else "- Define the concept\n- Explain why it matters\n- Give a real-world example"
    )

    prompt = _PROMPT_TEMPLATE.format(
        question=state.user_question,
        topic=state.topic,
        learning_steps=steps_text,
    )

    try:
        raw = generate(
            model=MODELS["explainer"],
            prompt=prompt,
            agent_name="explainer",
        )
        simple, why, intuition = _parse_sections(raw)
        state.theory_text = simple
        state.why_it_matters = why
        state.intuition_example = intuition
    except RuntimeError as exc:
        state.errors.append(f"Explainer: {exc}")
        state.theory_text = (
            f"Could not generate explanation for '{state.topic}'. "
            "Please check that Ollama is running and the model is pulled."
        )

    state.agents_run.append("explainer")
    return state
