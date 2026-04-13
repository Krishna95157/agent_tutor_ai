# AgentTutor AI

A multi-agent educational assistant that explains **Artificial Intelligence**, **Machine Learning**, **Deep Learning**, and **Data Mining** to students using a theory-first pipeline of four sequential agents.

Every answer follows a strict 7-section format:

1. Simple Explanation
2. Why It Matters
3. Intuition / Example
4. Code Example *(only when needed)*
5. Code Explanation *(only when code is present)*
6. Key Points / Common Mistakes
7. Final Takeaway

---

## How It Works

```
Student Question
       ↓
 Planner Agent      — understands the question, sets needs_theory / needs_code / needs_review,
                      produces an ordered list of learning steps
       ↓
Explainer Agent     — writes three sections:
                        1. Simple Explanation
                        2. Why It Matters
                        3. Intuition / Example
       ↓
Developer Agent     — writes a short Python example + step-by-step code explanation
                      (skipped automatically when the planner sets needs_code = false)
       ↓
  Critic Agent      — reviews the answer, flags clarity issues, lists key points /
                      common mistakes, and rewrites the theory when needed
       ↓
 Final Response     — all 7 sections assembled into clean Markdown and rendered in the UI
```

All agents run **sequentially, one at a time** — safe for MacBook Air M1 (8 GB RAM).

---

## Requirements

- macOS (tested on M1 / M2) with [Ollama](https://ollama.com) installed
- Python 3.11+

---

## Setup

```bash
# 1. Install Python dependencies
pip install -r requirements.txt

# 2. Start Ollama (open the app or run in terminal)
ollama serve

# 3. Pull the required models
ollama pull gemma3:1b
ollama pull deepseek-coder:1.3b
ollama pull phi4-mini

# 4. Run the Flask web server
python3 server.py
```

Then open [http://localhost:5000](http://localhost:5000) in your browser.

---

## Models

| Agent     | Model                | Role                                      |
|-----------|----------------------|-------------------------------------------|
| Planner   | `gemma3:1b`          | Parses question, builds learning plan     |
| Explainer | `gemma3:1b`          | Writes theory in 3 labeled sections       |
| Developer | `deepseek-coder:1.3b`| Writes Python code + step-by-step explanation |
| Critic    | `phi4-mini:latest`   | Reviews answer, adds key points, revises if needed |

Swap any model by editing `app/config.py`. Fallback models are also configured there.

---

## Answer Format

Every answer the system produces follows this exact template:

```
# Topic: <Topic Name>

## 1. Simple Explanation
Explain in simple words — beginner-friendly.

## 2. Why It Matters
Why this concept is important in AI / ML / DL / Data Mining.

## 3. Intuition / Example
Real-world analogy or simple concrete example.

## 4. Code Example          ← only when code was requested or needed
Short Python code with inline comments.

## 5. Code Explanation       ← only when code is present
Numbered steps explaining what the code does.

## 6. Key Points / Common Mistakes
Important notes and mistakes students commonly make.

## 7. Final Takeaway
1–2 line summary.
```

---

## Pipeline State

The `PipelineState` dataclass (`app/state.py`) carries all data between agents:

| Field               | Set by    | Description                                      |
|---------------------|-----------|--------------------------------------------------|
| `topic`             | Planner   | Detected topic name                              |
| `question_type`     | Planner   | concept_explanation / comparison / how_to / example_request |
| `needs_code`        | Planner   | Whether a code example is required               |
| `learning_steps`    | Planner   | Ordered list of learning steps                   |
| `theory_text`       | Explainer | Section 1 — Simple Explanation                   |
| `why_it_matters`    | Explainer | Section 2 — Why It Matters                       |
| `intuition_example` | Explainer | Section 3 — Intuition / Example                  |
| `code_snippet`      | Developer | Section 4 — Python code                          |
| `code_explanation`  | Developer | Section 5 — Step-by-step code explanation        |
| `key_points`        | Critic    | Section 6 — Key points / common mistakes         |
| `missing_points`    | Critic    | Extra concepts worth knowing                     |
| `revised_theory`    | Critic    | Rewritten Simple Explanation (when needed)       |

---

## API

The Flask server exposes one endpoint:

### `POST /api/pipeline`

**Request body:**
```json
{ "question": "Explain gradient descent with a Python example." }
```

**Response:**
```json
{
  "blocked": false,
  "question": "...",
  "planner": {
    "topic": "Gradient Descent",
    "question_type": "concept_explanation",
    "needs_theory": true,
    "needs_example": true,
    "needs_code": true,
    "needs_review": true,
    "learning_steps": ["Define gradient descent", "..."]
  },
  "explainer": {
    "theory": "...",
    "why_it_matters": "...",
    "intuition_example": "..."
  },
  "developer": {
    "code": "...",
    "purpose": "...",
    "code_explanation": "...",
    "skipped": false
  },
  "critic": {
    "clarity_check": "good",
    "missing_points": ["..."],
    "key_points": ["..."],
    "code_feedback": "...",
    "revision_needed": false,
    "revised_theory": null
  },
  "final": "...full 7-section Markdown...",
  "agents_run": ["planner", "explainer", "developer", "critic"],
  "errors": []
}
```

If the question is out of scope, the response contains `"blocked": true` and a message.

---

## Domain Guard

The system only answers questions in these domains:

- Artificial Intelligence
- Machine Learning
- Deep Learning
- Data Mining
- Math & Foundations (linear algebra, probability, statistics, information theory, optimization)
- Practical ML Workflow (MLOps, deployment, RAG, prompt engineering)

Off-topic questions are blocked before any agent runs.

---

## Project Structure

```
agent_tutor_ai/
├── server.py                   ← Flask web server (entry point)
├── run.py                      ← CLI runner (no UI)
├── benchmark.py                ← Batch benchmark runner
├── requirements.txt
│
├── app/
│   ├── config.py               ← Model assignments, token caps, allowed domains
│   ├── state.py                ← PipelineState dataclass (shared between agents)
│   ├── workflow.py             ← Sequential pipeline orchestrator
│   ├── router.py               ← Domain guard
│   │
│   ├── agents/
│   │   ├── planner.py          ← Parses question → JSON learning plan
│   │   ├── explainer.py        ← Produces 3-section theory explanation
│   │   ├── developer.py        ← Produces code + step-by-step explanation
│   │   └── critic.py           ← Produces key points, optional revised theory
│   │
│   ├── prompts/
│   │   ├── planner.txt
│   │   ├── explainer.txt
│   │   ├── developer.txt
│   │   └── critic.txt
│   │
│   ├── services/
│   │   ├── ollama_client.py    ← Talks to Ollama REST API
│   │   └── formatter.py        ← Assembles the 7-section Markdown response
│   │
│   └── utils/
│       ├── validators.py       ← is_in_scope(), sanitise_question()
│       └── helpers.py
│
├── templates/
│   └── index.html              ← Single-page HTML shell
│
├── static/
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── app.js              ← All UI logic (no framework, plain JS)
│
├── tests/
│   ├── test_agents.py
│   ├── test_workflow.py
│   └── test_output_format.py
│
└── outputs/
    └── benchmark_report.json
```

---

## Running Tests

```bash
pytest tests/ -v
```

---

## Configuration

Edit `app/config.py` to change models, token caps, or allowed domains:

```python
MODELS = {
    "planner":   "gemma3:1b",
    "explainer": "gemma3:1b",
    "developer": "deepseek-coder:1.3b",
    "critic":    "phi4-mini:latest",
}

MAX_TOKENS = {
    "planner":  400,
    "explainer": 600,
    "developer": 400,
    "critic":   400,
}
```

---

## Contributors

- **Vamsi Krishna** ([@Krishna95157](https://github.com/Krishna95157)) — Project author
