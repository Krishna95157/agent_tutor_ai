"""
Shared pipeline state passed between agents.
Using a plain dataclass keeps things simple and RAM-friendly.
"""

from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class PipelineState:
    # --- input ---
    user_question: str = ""

    # --- planner output ---
    topic: str = ""
    question_type: str = ""          # concept_explanation | comparison | how_to | example_request
    needs_theory: bool = True
    needs_example: bool = True
    needs_code: bool = False
    needs_review: bool = True
    learning_steps: List[str] = field(default_factory=list)

    # --- explainer output ---
    theory_text: str = ""          # section 1: simple explanation
    why_it_matters: str = ""       # section 2: why it matters
    intuition_example: str = ""    # section 3: intuition / example

    # --- developer output ---
    code_snippet: Optional[str] = None
    code_purpose: str = ""
    code_explanation: str = ""     # section 5: step-by-step code explanation

    # --- critic output ---
    clarity_check: str = ""
    missing_points: List[str] = field(default_factory=list)
    key_points: List[str] = field(default_factory=list)   # section 6: key points / common mistakes
    code_feedback: str = ""
    revision_needed: bool = False
    revised_theory: Optional[str] = None

    # --- pipeline metadata ---
    agents_run: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
