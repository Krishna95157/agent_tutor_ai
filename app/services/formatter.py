"""
Assembles the final student-facing response from the pipeline state.
Follows the exact 7-section template:
  1. Simple Explanation
  2. Why It Matters
  3. Intuition / Example
  4. Code Example  (only when present)
  5. Code Explanation  (only when present)
  6. Key Points / Common Mistakes  (from critic)
  7. Final Takeaway
"""

from app.state import PipelineState


def build_final_response(state: PipelineState) -> str:
    """Return a clean Markdown string ready for display."""
    parts = []
    topic = state.topic or "this concept"

    # 1. Simple Explanation
    theory = state.revised_theory if state.revised_theory else state.theory_text
    if theory:
        parts.append("## 🧠 1. Simple Explanation\n" + theory.strip())

    # 2. Why It Matters
    if state.why_it_matters:
        parts.append("## 🎯 2. Why It Matters\n" + state.why_it_matters.strip())

    # 3. Intuition / Example
    if state.intuition_example:
        parts.append("## 🔍 3. Intuition / Example\n" + state.intuition_example.strip())

    # 4. Code Example (only when present)
    if state.code_snippet:
        purpose_line = f"*{state.code_purpose}*\n\n" if state.code_purpose else ""
        parts.append(
            f"## ⚙️ 4. Code Example\n{purpose_line}```python\n{state.code_snippet.strip()}\n```"
        )

    # 5. Code Explanation (only when present)
    if state.code_snippet and state.code_explanation:
        parts.append("## 🔍 5. Code Explanation\n" + state.code_explanation.strip())

    # 6. Key Points / Common Mistakes — only key_points, never fall back to missing_points
    if state.key_points:
        items = "\n".join(f"- {pt}" for pt in state.key_points)
        parts.append("## ⚠️ 6. Key Points / Common Mistakes\n" + items)

    # Also Worth Knowing — missing_points shown separately
    if state.missing_points:
        items = "\n".join(f"- {pt}" for pt in state.missing_points)
        parts.append("## 💡 Also Worth Knowing\n" + items)

    # 7. Final Takeaway
    parts.append(
        f"## ✅ 7. Final Takeaway\n"
        f"**{topic.title()}** is an important concept in AI, ML, DL, and Data Mining. "
        f"Understanding it well will help you build stronger models and reason about complex problems."
    )

    return "\n\n---\n\n".join(parts)
