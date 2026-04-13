"""
AgentTutor AI — Flask web server.
Run: python3 server.py
Opens at: http://localhost:5000
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from flask import Flask, request, jsonify, render_template
from app.state import PipelineState
from app.agents import planner, explainer, developer, critic
from app.services.formatter import build_final_response
from app.utils.validators import is_in_scope, sanitise_question

app = Flask(__name__, static_folder="static", template_folder="templates")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/pipeline", methods=["POST"])
def run_pipeline():
    data = request.get_json(force=True)
    question = sanitise_question(data.get("question", ""))

    if not question:
        return jsonify({"error": "No question provided"}), 400

    # Off-topic guard
    if not is_in_scope(question):
        return jsonify({
            "blocked": True,
            "message": (
                "This assistant only covers Artificial Intelligence, "
                "Machine Learning, Deep Learning, and Data Mining. "
                "Please ask something in those areas."
            ),
        })

    state = PipelineState(user_question=question)

    # Run all agents sequentially — one at a time (RAM-safe for M1)
    planner.run(state)
    explainer.run(state)
    developer.run(state)
    critic.run(state)

    final_md = build_final_response(state)

    return jsonify({
        "blocked": False,
        "question": question,
        "planner": {
            "topic": state.topic,
            "question_type": state.question_type,
            "needs_theory": state.needs_theory,
            "needs_example": state.needs_example,
            "needs_code": state.needs_code,
            "needs_review": state.needs_review,
            "learning_steps": state.learning_steps,
        },
        "explainer": {
            "theory": state.theory_text,
            "why_it_matters": state.why_it_matters,
            "intuition_example": state.intuition_example,
        },
        "developer": {
            "code": state.code_snippet,
            "purpose": state.code_purpose,
            "code_explanation": state.code_explanation,
            "skipped": not state.needs_code,
        },
        "critic": {
            "clarity_check": state.clarity_check,
            "missing_points": state.missing_points,
            "key_points": state.key_points,
            "code_feedback": state.code_feedback,
            "revision_needed": state.revision_needed,
            "revised_theory": state.revised_theory,
        },
        "final": final_md,
        "agents_run": state.agents_run,
        "errors": state.errors,
    })


if __name__ == "__main__":
    print("\n  AgentTutor AI is running!")
    print("  Open your browser at: http://localhost:5000\n")
    app.run(debug=False, port=5000, host="0.0.0.0")
