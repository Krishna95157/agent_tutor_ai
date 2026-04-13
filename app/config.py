"""
Central configuration for AgentTutor AI.
All model assignments and Ollama settings live here.
"""

OLLAMA_BASE_URL = "http://localhost:11434"

# Model assigned to each agent — swap names here if you pull different models
MODELS = {
    "planner":  "gemma3:1b",
    "explainer": "gemma3:1b",
    "developer": "deepseek-coder:1.3b",
    "critic":   "phi4-mini:latest",   # phi4-mini:latest available locally; swap to phi4-mini:3.8b-q4_K_M if pulled
}

# Fallback map: if a preferred model isn't pulled, use the fallback automatically.
_FALLBACKS = {
    "deepseek-coder:1.3b": "gemma2:2b",
    "gemma3:1b": "gemma2:2b",
}

# Safety caps so outputs stay short and RAM stays low
MAX_TOKENS = {
    "planner":  400,
    "explainer": 600,
    "developer": 400,
    "critic":   400,
}

# Topics the system is allowed to answer about
ALLOWED_DOMAINS = [
    "artificial intelligence", "machine learning", "deep learning", "data mining",
    "neural network", "reinforcement learning", "natural language processing",
    "computer vision", "robotics", "optimization", "linear algebra", "probability",
    "statistics", "information theory", "supervised", "unsupervised", "regression",
    "classification", "clustering", "dimensionality reduction", "feature",
    "gradient descent", "backpropagation", "transformer", "attention", "embedding",
    "convolutional", "recurrent", "lstm", "gru", "autoencoder", "generative",
    "diffusion", "foundation model", "fine-tuning", "transfer learning",
    "overfitting", "underfitting", "regularization", "cross-validation",
    "random forest", "decision tree", "support vector", "k-nearest", "naive bayes",
    "boosting", "bagging", "ensemble", "xgboost", "adaboost",
    "association rule", "apriori", "fp-growth", "anomaly detection", "pca",
    "t-sne", "umap", "data warehouse", "olap", "sentiment analysis",
    "knowledge graph", "bayesian", "markov", "q-learning", "policy",
    "search algorithm", "heuristic", "a* search", "minimax", "alpha-beta",
    "constraint satisfaction", "propositional logic", "predicate logic",
    "inference", "expert system", "strips", "fuzzy logic",
    "rag", "vector database", "prompt engineering", "lora", "quantization",
    "mlops", "model deployment", "data preprocessing", "exploratory data analysis",
    "ai", "ml", "dl", "nlp", "cv",
]
