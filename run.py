"""
AgentTutor AI — simple CLI runner.
Test the backend without any UI.

Usage:
    python3 run.py
    python3 run.py "What is overfitting?"
"""

import sys
import os

# Make sure the project root is on the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.workflow import stream_pipeline


def main():
    if len(sys.argv) > 1:
        question = " ".join(sys.argv[1:])
    else:
        print("AgentTutor AI — Backend Test")
        print("=" * 50)
        question = input("Ask a question: ").strip()
        if not question:
            print("No question entered.")
            return

    print()
    print(f"Question: {question}")
    print("=" * 50)

    for event, payload in stream_pipeline(question):
        if event == "agent_start":
            print(f"\n[{payload}] working...", flush=True)
        elif event == "agent_done":
            print(f"[{payload}] done.", flush=True)
        elif event == "error":
            print(f"[WARNING] {payload}", flush=True)
        elif event == "result":
            print()
            print("=" * 50)
            print("FINAL ANSWER")
            print("=" * 50)
            print(payload)


if __name__ == "__main__":
    main()
