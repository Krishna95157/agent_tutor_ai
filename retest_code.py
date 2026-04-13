import sys, os, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from app.state import PipelineState
from app.agents import planner, explainer, developer, critic
from app.services.formatter import build_final_response

def run(label, q):
    print(f"\n{label}")
    print("-" * 50)
    state = PipelineState(user_question=q)
    t0 = time.perf_counter()
    planner.run(state)
    print(f"  needs_code = {state.needs_code}")
    print(f"  topic      = {state.topic}")
    explainer.run(state)
    developer.run(state)
    critic.run(state)
    elapsed = round(time.perf_counter() - t0, 2)
    result = build_final_response(state)
    has_code = "```python" in result
    print(f"  code in output = {has_code}")
    print(f"  latency        = {elapsed}s")
    print(f"  agents run     = {state.agents_run}")
    if has_code:
        start = result.index("```python") + 9
        end   = result.index("```", start)
        snippet = result[start:end].strip()
        print(f"\n  Code snippet:\n")
        for line in snippet.splitlines():
            print(f"    {line}")

run("Test 2 — Gradient descent + Python", "Explain gradient descent with a simple Python example.")
run("Test 5 — K-means + Python",          "What is k-means clustering? Show a Python example.")
