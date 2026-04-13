"""
AgentTutor AI — Streamlit front end.

Run with:
    streamlit run app/main.py
from the project root (agent_tutor_ai/).
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st

from app.services.ollama_client import is_model_available, list_models
from app.utils.helpers import log_error, log_info, save_trace
from app.utils.validators import sanitise_question
from app.workflow import stream_pipeline

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="AgentTutor AI",
    page_icon="🎓",
    layout="centered",
)

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.title("AgentTutor AI")
    st.caption("A theory-first multi-agent learning assistant for AI, ML, DL & Data Mining")

    st.divider()

    st.markdown("**Pipeline**")
    st.markdown(
        """
1. **Planner** — understands your question
2. **Explainer** — writes the theory
3. **Developer** — adds code *(only if useful)*
4. **Critic** — reviews & improves the answer
"""
    )

    st.divider()

    st.markdown("**Ollama Status**")
    models = list_models()
    if models:
        st.success(f"{len(models)} model(s) available")
        for m in models:
            st.caption(f"• {m}")
    else:
        st.error("Ollama not running or no models pulled.")
        st.caption("Start Ollama, then pull: `ollama pull gemma3:1b`")

    st.divider()
    st.caption("Runs fully offline on your machine via Ollama.")


# ── Header ────────────────────────────────────────────────────────────────────
st.title("AgentTutor AI")
st.markdown(
    "Ask any question about **Artificial Intelligence**, **Machine Learning**, "
    "**Deep Learning**, or **Data Mining** — and four specialised agents will "
    "explain it step by step."
)

# ── Example questions ─────────────────────────────────────────────────────────
st.markdown("**Example questions:**")
examples = [
    "What is overfitting and how do we fix it?",
    "Explain gradient descent with a simple Python example.",
    "What is the difference between machine learning and deep learning?",
    "How does a CNN process images?",
    "Explain k-means clustering.",
    "What is attention mechanism in transformers?",
]
cols = st.columns(3)
selected_example = None
for i, ex in enumerate(examples):
    if cols[i % 3].button(ex, use_container_width=True):
        selected_example = ex

# ── Question input ────────────────────────────────────────────────────────────
st.divider()
default_text = selected_example if selected_example else ""
question_input = st.text_area(
    "Your question",
    value=default_text,
    placeholder="e.g. What is gradient descent?",
    height=80,
    max_chars=500,
    label_visibility="collapsed",
)

ask_col, clear_col = st.columns([4, 1])
ask_btn = ask_col.button("Ask AgentTutor", type="primary", use_container_width=True)
clear_btn = clear_col.button("Clear", use_container_width=True)

if clear_btn:
    st.rerun()

# ── Pipeline execution ────────────────────────────────────────────────────────
if ask_btn and question_input.strip():
    question = sanitise_question(question_input)
    log_info(f"New question: {question}")

    st.divider()
    st.markdown("### Pipeline Running")

    # Status placeholders for each agent
    agent_statuses = {
        "Planner Agent": st.empty(),
        "Explainer Agent": st.empty(),
        "Developer Agent": st.empty(),
        "Critic Agent": st.empty(),
    }

    for name, placeholder in agent_statuses.items():
        placeholder.markdown(f"⬜ **{name}** — waiting")

    result_placeholder = st.empty()
    final_md = None
    final_state = None

    active_agent = None

    for event, payload in stream_pipeline(question):
        if event == "agent_start":
            active_agent = payload
            if active_agent in agent_statuses:
                agent_statuses[active_agent].markdown(
                    f"🔄 **{active_agent}** — working..."
                )

        elif event == "agent_done":
            if active_agent in agent_statuses:
                agent_statuses[active_agent].markdown(
                    f"✅ **{active_agent}** — done"
                )
            active_agent = None

        elif event == "error":
            log_error(payload)
            st.warning(f"⚠️ {payload}")

        elif event == "result":
            final_md = payload

    # ── Display final answer ──────────────────────────────────────────────────
    if final_md:
        st.divider()
        st.markdown("### Answer")
        st.markdown(final_md)

        # Save trace for logging
        try:
            from app.workflow import run_pipeline as _rp  # import to get state
            # We already ran stream_pipeline; rebuild state from scratch would
            # re-run the models. Instead we log what we can.
            log_info("Pipeline completed successfully.")
        except Exception:
            pass

elif ask_btn and not question_input.strip():
    st.warning("Please type a question first.")

# ── Footer ────────────────────────────────────────────────────────────────────
st.divider()
st.caption(
    "AgentTutor AI · Runs locally via Ollama · "
    "Covers AI, ML, Deep Learning, and Data Mining only"
)
