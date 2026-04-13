"""
AgentTutor AI — benchmark runner.
Tests multiple questions, measures latency per agent and total,
and scores output quality with simple heuristics.
"""

import sys
import os
import time
import json
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.state import PipelineState
from app.utils.validators import is_in_scope
from app.agents import planner, explainer, developer, critic
from app.services.formatter import build_final_response

# ── Test cases ────────────────────────────────────────────────────────────────
TEST_CASES = [
    {
        "id": 1,
        "question": "What is overfitting?",
        "expect_code": False,
        "expect_keywords": ["training", "model", "generalize", "noise"],
        "domain": "Machine Learning",
    },
    {
        "id": 2,
        "question": "Explain gradient descent with a simple Python example.",
        "expect_code": True,
        "expect_keywords": ["gradient", "loss", "learning rate", "optimiz"],
        "domain": "Machine Learning",
    },
    {
        "id": 3,
        "question": "What is the difference between machine learning and deep learning?",
        "expect_code": False,
        "expect_keywords": ["machine learning", "deep learning", "neural", "data"],
        "domain": "AI / ML",
    },
    {
        "id": 4,
        "question": "Explain the attention mechanism in transformers.",
        "expect_code": False,
        "expect_keywords": ["attention", "query", "key", "value", "weight"],
        "domain": "Deep Learning",
    },
    {
        "id": 5,
        "question": "What is k-means clustering? Show a Python example.",
        "expect_code": True,
        "expect_keywords": ["cluster", "centroid", "k-means", "assign"],
        "domain": "Data Mining",
    },
    {
        "id": 6,
        "question": "What is the capital of France?",   # off-topic guard test
        "expect_code": False,
        "expect_keywords": ["only", "covers", "focuses"],
        "domain": "OFF-TOPIC (should be rejected)",
    },
]

SEP = "=" * 65


def score_output(response: str, keywords: list, expect_code: bool, state: PipelineState) -> dict:
    """Simple heuristic scoring — no external model needed."""
    text_lower = response.lower()

    # Keyword coverage (0–100)
    hits = sum(1 for kw in keywords if kw.lower() in text_lower)
    keyword_score = round((hits / len(keywords)) * 100) if keywords else 100

    # Structure check
    has_explanation = "## simple explanation" in text_lower or "## explanation" in text_lower
    has_takeaway    = "## final takeaway" in text_lower
    has_code        = "```python" in response

    structure_score = 0
    if has_explanation: structure_score += 40
    if has_takeaway:    structure_score += 30
    if len(response) > 200: structure_score += 30

    # Code expectation match
    code_match = (has_code == expect_code)

    # No errors
    error_free = len(state.errors) == 0

    # Composite score (weighted)
    composite = round(keyword_score * 0.5 + structure_score * 0.4 + (10 if code_match else 0))

    return {
        "keyword_score": keyword_score,
        "keyword_hits": f"{hits}/{len(keywords)}",
        "structure_score": structure_score,
        "code_expectation_met": code_match,
        "error_free": error_free,
        "composite": min(composite, 100),
    }


def run_timed_pipeline(question: str):
    """Run the pipeline recording per-agent latency."""
    state = PipelineState(user_question=question.strip())
    timings = {}

    # Domain guard
    if not is_in_scope(question):
        state.theory_text = (
            "This system covers Artificial Intelligence, Machine Learning, "
            "Deep Learning, and Data Mining only. Please ask a question in those areas."
        )
        state.agents_run.append("router (blocked)")
        return build_final_response(state), state, {"router": 0.0}

    steps = [
        ("planner",   planner.run),
        ("explainer", explainer.run),
        ("developer", developer.run),
        ("critic",    critic.run),
    ]

    for name, fn in steps:
        t0 = time.perf_counter()
        fn(state)
        timings[name] = round(time.perf_counter() - t0, 2)

    return build_final_response(state), state, timings


def main():
    print(SEP)
    print("  AgentTutor AI — Benchmark Report")
    print(f"  {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(SEP)

    results = []

    for tc in TEST_CASES:
        print(f"\nTest {tc['id']}: {tc['question']}")
        print(f"Domain : {tc['domain']}")
        print("-" * 65)

        wall_start = time.perf_counter()
        response, state, timings = run_timed_pipeline(tc["question"])
        wall_total = round(time.perf_counter() - wall_start, 2)

        scores = score_output(response, tc["expect_keywords"], tc["expect_code"], state)

        # Per-agent latency
        print("Latency per agent:")
        for agent, secs in timings.items():
            bar = "#" * int(secs * 2)
            print(f"  {agent:<12} {secs:>5.2f}s  {bar}")
        print(f"  {'TOTAL':<12} {wall_total:>5.2f}s")

        # Quality scores
        print("Quality scores:")
        print(f"  Keyword coverage : {scores['keyword_score']:>3}%  ({scores['keyword_hits']} keywords found)")
        print(f"  Structure score  : {scores['structure_score']:>3}%")
        print(f"  Code expectation : {'PASS' if scores['code_expectation_met'] else 'FAIL'}")
        print(f"  Error free       : {'YES' if scores['error_free'] else 'NO  ' + str(state.errors)}")
        print(f"  COMPOSITE SCORE  : {scores['composite']:>3}%")

        print("Agents run:", " -> ".join(state.agents_run))

        # Show trimmed response
        preview = response[:400].replace("\n", " ").strip()
        print(f"Preview: {preview}...")

        results.append({
            "id": tc["id"],
            "question": tc["question"],
            "domain": tc["domain"],
            "latency_total": wall_total,
            "timings": timings,
            "scores": scores,
            "agents_run": state.agents_run,
        })

    # ── Summary table ─────────────────────────────────────────────────────────
    print()
    print(SEP)
    print("  SUMMARY")
    print(SEP)
    print(f"{'#':<4} {'Domain':<22} {'Latency':>8} {'Composite':>10} {'Code':>6} {'Errors':>7}")
    print("-" * 65)

    total_latency = 0
    total_composite = 0
    in_scope = [r for r in results if "blocked" not in " ".join(r["agents_run"])]

    for r in results:
        s = r["scores"]
        blocked = "blocked" in " ".join(r["agents_run"])
        code_ok = "PASS" if s["code_expectation_met"] else "FAIL"
        err_ok  = "OK" if s["error_free"] else "ERR"
        label   = "REJECTED" if blocked else f"{s['composite']}%"
        total_latency += r["latency_total"]
        if not blocked:
            total_composite += s["composite"]
        print(f"{r['id']:<4} {r['domain']:<22} {r['latency_total']:>7.2f}s {label:>10} {code_ok:>6} {err_ok:>7}")

    print("-" * 65)
    avg_latency   = round(total_latency / len(results), 2)
    avg_composite = round(total_composite / len(in_scope), 1) if in_scope else 0
    print(f"{'AVG':<4} {'':<22} {avg_latency:>7.2f}s {avg_composite:>9}%")
    print()
    print(f"Total test cases : {len(results)}")
    print(f"In-scope tests   : {len(in_scope)}")
    print(f"Off-topic blocked: {len(results) - len(in_scope)}")
    print(f"Avg quality score: {avg_composite}%")
    print(f"Avg latency      : {avg_latency}s per question")
    print(SEP)

    # Save JSON report
    report_path = os.path.join("outputs", "benchmark_report.json")
    os.makedirs("outputs", exist_ok=True)
    with open(report_path, "w") as f:
        json.dump(results, f, indent=2)
    print(f"Full report saved to: {report_path}")


if __name__ == "__main__":
    main()
