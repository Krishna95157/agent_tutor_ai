"""
Miscellaneous helper utilities.
"""

import json
import logging
from datetime import datetime
from pathlib import Path

LOG_DIR = Path(__file__).parent.parent.parent / "outputs" / "logs"
TRACE_DIR = Path(__file__).parent.parent.parent / "outputs" / "traces"

# Ensure directories exist at import time
LOG_DIR.mkdir(parents=True, exist_ok=True)
TRACE_DIR.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    filename=str(LOG_DIR / "pipeline.log"),
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)


def log_info(message: str) -> None:
    logging.info(message)


def log_error(message: str) -> None:
    logging.error(message)


def save_trace(state) -> Path:
    """
    Serialise PipelineState to a JSON trace file in outputs/traces/.
    Returns the path of the written file.
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_topic = "".join(c if c.isalnum() else "_" for c in state.topic[:30])
    filename = TRACE_DIR / f"trace_{timestamp}_{safe_topic}.json"

    trace = {
        "timestamp": timestamp,
        "user_question": state.user_question,
        "topic": state.topic,
        "question_type": state.question_type,
        "needs_code": state.needs_code,
        "agents_run": state.agents_run,
        "errors": state.errors,
        "learning_steps": state.learning_steps,
        "theory_preview": state.theory_text[:200],
        "code_present": state.code_snippet is not None,
        "revision_needed": state.revision_needed,
        "clarity_check": state.clarity_check,
        "missing_points": state.missing_points,
    }

    filename.write_text(json.dumps(trace, indent=2))
    return filename


def format_agents_run(agents_run: list) -> str:
    """Return a human-readable pipeline summary string."""
    return " → ".join(agents_run) if agents_run else "none"
