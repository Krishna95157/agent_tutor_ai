// ================================================================
//  AgentTutor AI — Frontend Application
//  All UI is built here. HTML file is just the shell.
// ================================================================

// ── TOPICS DATA ─────────────────────────────────────────────────
const DOMAINS = {
  "Artificial Intelligence": {
    color: "#a78bfa", bg: "rgba(167,139,250,0.1)", icon: "🤖",
    topics: [
      "Artificial Intelligence","Intelligent agents","Rational agents",
      "Agent environments","PEAS framework","State space search",
      "Uninformed search","Breadth-first search","Depth-first search",
      "Uniform cost search","Iterative deepening search","Heuristic search",
      "Greedy best-first search","A* search","Local search","Hill climbing",
      "Simulated annealing","Constraint satisfaction problems","Backtracking search",
      "Game playing","Minimax algorithm","Alpha-beta pruning",
      "Knowledge representation","Propositional logic","Predicate logic",
      "Inference","Forward chaining","Backward chaining","Expert systems",
      "Planning","STRIPS planning","Decision making","Utility theory",
      "Bayesian reasoning","Markov decision processes","Reinforcement learning basics",
      "Q-learning","Policy iteration","Value iteration","Multi-agent systems",
      "Knowledge graphs","Reasoning under uncertainty","Fuzzy logic",
      "Natural language processing basics","Computer vision basics",
      "Robotics basics","Explainable AI","Ethics in AI",
      "Responsible AI","AI bias","Human-AI interaction"
    ]
  },
  "Machine Learning": {
    color: "#60a5fa", bg: "rgba(96,165,250,0.1)", icon: "🧠",
    topics: [
      "Machine learning overview","Types of machine learning",
      "Supervised learning","Unsupervised learning","Semi-supervised learning",
      "Self-supervised learning","Regression","Classification","Clustering",
      "Dimensionality reduction","Feature engineering","Feature selection",
      "Feature extraction","Training data","Validation data","Test data",
      "Data splitting","Cross-validation","Bias","Variance",
      "Bias-variance tradeoff","Overfitting","Underfitting","Regularization",
      "L1 regularization","L2 regularization","Model evaluation",
      "Confusion matrix","Accuracy","Precision","Recall","F1-score",
      "ROC curve","AUC","Mean squared error","Mean absolute error",
      "R-squared","Loss functions","Optimization","Gradient descent",
      "Batch gradient descent","Stochastic gradient descent",
      "Mini-batch gradient descent","Learning rate","Hyperparameters",
      "Hyperparameter tuning","Grid search","Random search",
      "Bayesian optimization","Linear regression","Multiple linear regression",
      "Logistic regression","Polynomial regression","Decision trees",
      "Random forests","Bagging","Boosting","AdaBoost",
      "Gradient boosting","XGBoost","Support vector machines",
      "K-nearest neighbors","Naive Bayes","Ensemble learning",
      "Model interpretability","SHAP","LIME","Class imbalance",
      "Data leakage","Pipelines in ML","Time series forecasting",
      "Anomaly detection","Recommendation systems","Online learning",
      "Transfer learning basics"
    ]
  },
  "Deep Learning": {
    color: "#22d3ee", bg: "rgba(34,211,238,0.1)", icon: "🔬",
    topics: [
      "Artificial neural networks","Biological neuron vs artificial neuron",
      "Perceptron","Multilayer perceptron","Input layer","Hidden layer",
      "Output layer","Weights and biases","Activation functions",
      "Sigmoid","Tanh","ReLU","Leaky ReLU","Softmax",
      "Forward propagation","Backpropagation","Chain rule in deep learning",
      "Loss functions in deep learning","Mean squared error loss",
      "Cross-entropy loss","Optimizers","SGD","Momentum","RMSProp",
      "Adam","Learning rate scheduling","Epochs","Batches","Batch size",
      "Weight initialization","Xavier initialization","He initialization",
      "Vanishing gradients","Exploding gradients","Dropout",
      "Batch normalization","Layer normalization","Early stopping",
      "Deep feedforward networks","Convolutional neural networks",
      "Convolution operation","Filters and kernels","Stride","Padding",
      "Pooling","Max pooling","Average pooling","Feature maps",
      "Image classification","Object detection basics","Semantic segmentation basics",
      "Recurrent neural networks","Sequence modeling","Vanishing gradient in RNNs",
      "LSTM","GRU","Attention mechanism","Self-attention","Transformers",
      "Encoder-decoder architecture","Positional encoding","Embeddings",
      "Word embeddings","Tokenization","Language models","Fine-tuning",
      "Transfer learning in deep learning","Autoencoders",
      "Variational autoencoders","Generative adversarial networks",
      "Diffusion models basics","Seq2Seq models","Vision transformers",
      "Multimodal learning","Representation learning","Metric learning",
      "Contrastive learning","Zero-shot learning","Few-shot learning",
      "Foundation models","Prompting basics","Parameter-efficient fine-tuning",
      "LoRA","Quantization basics"
    ]
  },
  "Data Mining": {
    color: "#fb923c", bg: "rgba(251,146,60,0.1)", icon: "📊",
    topics: [
      "Data mining overview","Knowledge discovery in databases",
      "Data cleaning","Data integration","Data transformation",
      "Data reduction","Data preprocessing","Missing value handling",
      "Noise removal","Outlier detection","Descriptive analytics",
      "Predictive analytics","Association rule mining","Frequent itemsets",
      "Apriori algorithm","FP-growth","Support","Confidence","Lift",
      "Clustering in data mining","K-means clustering","Hierarchical clustering",
      "DBSCAN","Density-based clustering","Cluster validity",
      "Classification in data mining","Regression in data mining",
      "Sequential pattern mining","Web mining","Text mining","Opinion mining",
      "Sentiment analysis basics","Anomaly detection in data mining",
      "Pattern discovery","Data warehousing","OLAP",
      "Dimensionality reduction in data mining","Principal component analysis",
      "t-SNE","UMAP","Data visualization basics","Market basket analysis",
      "Customer segmentation","Fraud detection","Recommendation mining",
      "Graph mining","Social network analysis","Temporal data mining",
      "Spatial data mining","Stream data mining","Big data mining",
      "Sampling","Discretization","Feature construction","Correlation analysis",
      "Causal analysis basics","Rule-based mining","Pattern evaluation",
      "Interestingness measures","Imbalanced data handling",
      "Scalable mining methods","Privacy-preserving data mining"
    ]
  },
  "Math & Foundations": {
    color: "#4ade80", bg: "rgba(74,222,128,0.1)", icon: "📐",
    topics: [
      "Linear algebra for ML","Vectors","Matrices","Tensors",
      "Matrix multiplication","Dot product","Eigenvalues","Eigenvectors",
      "Singular value decomposition","Probability basics",
      "Conditional probability","Bayes theorem","Random variables",
      "Probability distributions","Normal distribution","Bernoulli distribution",
      "Binomial distribution","Expectation","Variance","Covariance",
      "Statistics basics","Mean median mode","Standard deviation",
      "Correlation","Hypothesis testing basics","Optimization theory",
      "Partial derivatives","Gradients","Jacobian","Hessian",
      "Convex functions","Convex optimization","Information theory",
      "Entropy","Cross-entropy","KL divergence","Distance metrics",
      "Euclidean distance","Manhattan distance","Cosine similarity"
    ]
  },
  "Practical Workflow": {
    color: "#f472b6", bg: "rgba(244,114,182,0.1)", icon: "⚙️",
    topics: [
      "Problem formulation","Data collection","Data labeling",
      "Exploratory data analysis","Data preprocessing pipeline",
      "Model selection","Baseline models","Experiment tracking",
      "Reproducibility","Evaluation strategy","Error analysis",
      "Model deployment basics","Inference pipeline",
      "Monitoring model performance","Model drift","Data drift",
      "Retraining strategy","MLOps basics","Responsible deployment",
      "Interpretability in practice","Debugging ML models",
      "Benchmarking models","Latency","Throughput","Memory efficiency",
      "Model compression","Pruning","Quantization in deployment",
      "Edge AI basics","On-device AI basics","Local LLMs","RAG basics",
      "Vector databases","Embeddings in retrieval","Reranking",
      "Agentic AI basics","Tool use in agents","Multi-agent orchestration",
      "Prompt engineering","Structured output generation"
    ]
  }
};

const AGENT_META = {
  planner:   { icon: "📋", label: "Planner Agent",   color: "var(--planner)",   bg: "rgba(167,139,250,0.12)", role: "Understands your question and creates a learning plan" },
  explainer: { icon: "📖", label: "Explainer Agent", color: "var(--explainer)", bg: "rgba(96,165,250,0.12)",  role: "Explains the concept in simple, student-friendly language" },
  developer: { icon: "💻", label: "Developer Agent", color: "var(--developer)", bg: "rgba(52,211,153,0.12)",  role: "Writes a beginner Python example only when it helps" },
  critic:    { icon: "🔍", label: "Critic Agent",    color: "var(--critic)",    bg: "rgba(251,191,36,0.12)",  role: "Reviews the answer and improves it for clarity" },
  final:     { icon: "✨", label: "Final Answer",    color: "var(--final)",     bg: "rgba(244,114,182,0.12)", role: "The complete, clean answer ready to read and learn from" },
};

const EXAMPLE_QUESTIONS = [
  "What is overfitting and why does it happen?",
  "Explain gradient descent with a simple Python example.",
  "What is the difference between machine learning and deep learning?",
  "How does the attention mechanism in transformers work?",
  "What is k-means clustering? Show a Python example.",
  "Explain backpropagation in simple words.",
  "What is reinforcement learning?",
  "How does a convolutional neural network process images?",
];

// ── APP STATE ────────────────────────────────────────────────────
const state = {
  page: "topics",
  question: "",
  result: null,
  loading: false,
};

// ── DOM HELPERS ──────────────────────────────────────────────────
function el(tag, attrs = {}, ...children) {
  const node = document.createElement(tag);
  Object.entries(attrs).forEach(([k, v]) => {
    if (k === "class") node.className = v;
    else if (k === "style" && typeof v === "object") Object.assign(node.style, v);
    else if (k.startsWith("on")) node.addEventListener(k.slice(2), v);
    else node.setAttribute(k, v);
  });
  children.flat().forEach(c => {
    if (c == null) return;
    node.appendChild(typeof c === "string" ? document.createTextNode(c) : c);
  });
  return node;
}

function div(attrs, ...children) { return el("div", attrs, ...children); }
function span(attrs, ...children) { return el("span", attrs, ...children); }
function p(attrs, ...children) { return el("p", attrs, ...children); }
function h1(attrs, ...children) { return el("h1", attrs, ...children); }
function h2(attrs, ...children) { return el("h2", attrs, ...children); }
function h3(attrs, ...children) { return el("h3", attrs, ...children); }
function button(attrs, ...children) { return el("button", attrs, ...children); }
function input(attrs) { return el("input", attrs); }

// ── PYTHON SYNTAX HIGHLIGHTER ────────────────────────────────────
function highlightPython(code) {
  const escape = s => s.replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;");
  let html = "";
  const src = code;
  let i = 0;
  const KW = new Set([
    "def","class","import","from","return","if","else","elif","for","while",
    "in","not","and","or","with","as","try","except","finally","raise","pass",
    "break","continue","yield","lambda","is","global","nonlocal","del","assert",
    "True","False","None","async","await"
  ]);
  const BUILTINS = new Set([
    "print","range","len","list","dict","set","tuple","int","float","str",
    "bool","type","isinstance","enumerate","zip","map","filter","sorted",
    "reversed","sum","min","max","abs","round","open","input","super",
    "getattr","setattr","hasattr","any","all","iter","next"
  ]);

  while (i < src.length) {
    // Comment
    if (src[i] === "#") {
      let j = i; while (j < src.length && src[j] !== "\n") j++;
      html += `<span class="py-comment">${escape(src.slice(i,j))}</span>`;
      i = j; continue;
    }
    // String (triple first)
    if (src.slice(i,i+3) === '"""' || src.slice(i,i+3) === "'''") {
      const q = src.slice(i,i+3); let j = i+3;
      while (j < src.length && src.slice(j,j+3) !== q) j++;
      j += 3;
      html += `<span class="py-str">${escape(src.slice(i,j))}</span>`;
      i = j; continue;
    }
    if (src[i] === '"' || src[i] === "'") {
      const q = src[i]; let j = i+1;
      while (j < src.length && src[j] !== q && src[j] !== "\n") { if (src[j]==="\\") j++; j++; }
      j++;
      html += `<span class="py-str">${escape(src.slice(i,j))}</span>`;
      i = j; continue;
    }
    // Number
    if (/\d/.test(src[i]) && (i===0 || /[\W]/.test(src[i-1]))) {
      let j = i; while (j < src.length && /[\d._]/.test(src[j])) j++;
      html += `<span class="py-num">${escape(src.slice(i,j))}</span>`;
      i = j; continue;
    }
    // Word (keyword / builtin / function call / class)
    if (/[a-zA-Z_]/.test(src[i])) {
      let j = i; while (j < src.length && /\w/.test(src[j])) j++;
      const word = src.slice(i,j);
      const next = src.slice(j).trimStart();
      if (KW.has(word)) html += `<span class="py-kw">${escape(word)}</span>`;
      else if (BUILTINS.has(word)) html += `<span class="py-builtin">${escape(word)}</span>`;
      else if (next.startsWith("(")) html += `<span class="py-fn">${escape(word)}</span>`;
      else if (word[0] === word[0].toUpperCase() && word[0] !== word[0].toLowerCase())
        html += `<span class="py-cls">${escape(word)}</span>`;
      else html += escape(word);
      i = j; continue;
    }
    html += escape(src[i]); i++;
  }
  return html;
}

// ── MARKDOWN → HTML ──────────────────────────────────────────────
function renderMarkdown(text) {
  if (!text) return "";

  // Extract code blocks first (preserve them)
  const codeBlocks = [];
  text = text.replace(/```(\w*)\n?([\s\S]*?)```/g, (_, lang, code) => {
    codeBlocks.push({ lang: lang || "python", code: code.trim() });
    return `<<<CODE_BLOCK_${codeBlocks.length - 1}>>>`;
  });

  // Escape HTML in remaining text
  const esc = s => s.replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;");
  text = esc(text);

  // Headers
  text = text.replace(/^#### (.+)$/gm, "<h4>$1</h4>");
  text = text.replace(/^### (.+)$/gm, "<h3>$1</h3>");
  text = text.replace(/^## (.+)$/gm, "<h2>$1</h2>");
  text = text.replace(/^# (.+)$/gm, "<h1>$1</h1>");

  // Bold and italic
  text = text.replace(/\*\*\*(.+?)\*\*\*/g, "<strong><em>$1</em></strong>");
  text = text.replace(/\*\*(.+?)\*\*/g, "<strong>$1</strong>");
  text = text.replace(/\*(.+?)\*/g, "<em>$1</em>");

  // Inline code
  text = text.replace(/`([^`]+)`/g, '<code>$1</code>');

  // Horizontal rule
  text = text.replace(/^---$/gm, "<hr>");

  // Unordered lists
  text = text.replace(/((?:^[ \t]*[-*+] .+\n?)+)/gm, match => {
    const items = match.trim().split("\n").map(l => {
      const content = l.replace(/^[ \t]*[-*+] /, "");
      return `<li>${content}</li>`;
    }).join("");
    return `<ul>${items}</ul>`;
  });

  // Ordered lists
  text = text.replace(/((?:^\d+\. .+\n?)+)/gm, match => {
    const items = match.trim().split("\n").map(l => {
      const content = l.replace(/^\d+\. /, "");
      return `<li>${content}</li>`;
    }).join("");
    return `<ol>${items}</ol>`;
  });

  // Paragraphs — split by double newline
  const parts = text.split(/\n\n+/);
  text = parts.map(part => {
    part = part.trim();
    if (!part) return "";
    if (/^<(h[1-4]|ul|ol|hr)/.test(part)) return part;
    if (part.startsWith("&lt;&lt;&lt;CODE_BLOCK")) return part;
    return `<p>${part.replace(/\n/g, " ")}</p>`;
  }).join("\n");

  // Restore code blocks
  text = text.replace(/&lt;&lt;&lt;CODE_BLOCK_(\d+)&gt;&gt;&gt;/g, (_, idx) => {
    const { lang, code } = codeBlocks[parseInt(idx)];
    const highlighted = lang === "python" ? highlightPython(code) : code.replace(/</g,"&lt;").replace(/>/g,"&gt;");
    return buildCodeBlockHTML(lang, code, highlighted);
  });

  return text;
}

function buildCodeBlockHTML(lang, rawCode, highlighted) {
  const id = "cb_" + Math.random().toString(36).slice(2);
  return `
    <div class="code-block-wrap">
      <div class="code-block-header">
        <span class="code-lang">${lang}</span>
        <button class="copy-btn" onclick="copyCode('${id}')">Copy</button>
      </div>
      <pre class="code-block"><code id="${id}">${highlighted}</code></pre>
    </div>`;
}

window.copyCode = function(id) {
  const code = document.getElementById(id);
  if (!code) return;
  navigator.clipboard.writeText(code.innerText).then(() => {
    const btn = code.closest(".code-block-wrap").querySelector(".copy-btn");
    if (btn) { btn.textContent = "Copied!"; setTimeout(() => btn.textContent = "Copy", 1800); }
  });
};

// ── ROUTER ───────────────────────────────────────────────────────
function navigate(page) {
  state.page = page;
  updateNav();
  renderPage();
}

function updateNav() {
  document.querySelectorAll(".nav-item").forEach(item => {
    item.classList.remove("active");
    if (item.dataset.page === state.page) item.classList.add("active");
  });
  // Update topbar question
  const tq = document.getElementById("topbar-question");
  if (tq) {
    tq.textContent = state.question ? `"${state.question}"` : "";
    tq.style.display = state.question ? "block" : "none";
  }
}

// ── LAYOUT ───────────────────────────────────────────────────────
function buildLayout() {
  const root = document.getElementById("root");
  root.innerHTML = "";

  const pipelinePages = ["planner","explainer","developer","critic","final"];

  const navItems = [
    { page: "topics",   icon: "📚", label: "All Topics",      section: "main" },
    { page: "ask",      icon: "❓", label: "Ask a Question",   section: "main" },
    { divider: true,    label: "PIPELINE",                     section: "pipeline" },
    { page: "planner",  icon: "📋", label: "1. Planner",       section: "pipeline" },
    { page: "explainer",icon: "📖", label: "2. Explainer",     section: "pipeline" },
    { page: "developer",icon: "💻", label: "3. Developer",     section: "pipeline" },
    { page: "critic",   icon: "🔍", label: "4. Critic",        section: "pipeline" },
    { page: "final",    icon: "✨", label: "5. Final Answer",  section: "pipeline" },
  ];

  // Sidebar
  const sidebar = div({ class: "sidebar" },
    div({ class: "sidebar-logo" },
      div({ class: "logo-icon" }, "🎓"),
      div({ class: "logo-title" }, "AgentTutor AI"),
      div({ class: "logo-sub" }, "AI · ML · DL · Data Mining"),
    ),
  );

  navItems.forEach(item => {
    if (item.divider) {
      sidebar.appendChild(div({ class: "nav-section-label" }, item.label));
      return;
    }
    const isPipeline = pipelinePages.includes(item.page);
    const isDisabled = isPipeline && !state.result;
    const navEl = div({
      class: `nav-item${item.page === state.page ? " active" : ""}${isDisabled ? " disabled" : ""}`,
      "data-page": item.page,
      onclick: () => { if (!isDisabled) navigate(item.page); }
    },
      span({ class: "nav-icon" }, item.icon),
      span({}, item.label),
    );
    sidebar.appendChild(navEl);
  });

  sidebar.appendChild(div({ class: "sidebar-footer" },
    div({ class: "model-badge" },
      "Models running locally",
      span({}, "gemma3:1b · deepseek-coder:1.3b"),
      span({}, "phi4-mini · Ollama"),
    )
  ));

  // Main wrapper
  const topbar = div({ class: "topbar" },
    div({ class: "topbar-title" }, "AgentTutor AI"),
    div({ class: "topbar-question", id: "topbar-question", style: { display: "none" } }, ""),
  );

  const contentArea = div({ class: "page-content fade-in", id: "page-content" });

  const mainWrap = div({ class: "main-wrap" }, topbar, contentArea);

  root.appendChild(sidebar);
  root.appendChild(mainWrap);
}

// ── PIPELINE PROGRESS BAR ────────────────────────────────────────
function buildProgressBar(activePage) {
  const steps = [
    { page: "planner",   icon: "📋", label: "Plan" },
    { page: "explainer", icon: "📖", label: "Explain" },
    { page: "developer", icon: "💻", label: "Code" },
    { page: "critic",    icon: "🔍", label: "Review" },
    { page: "final",     icon: "✨", label: "Final" },
  ];

  const pages = ["planner","explainer","developer","critic","final"];
  const activeIdx = pages.indexOf(activePage);

  const bar = div({ class: "pipeline-progress" });
  steps.forEach((s, i) => {
    if (i > 0) bar.appendChild(span({ class: "prog-arrow" }, "→"));
    const isActive = s.page === activePage;
    const isDone   = i < activeIdx;
    const stepEl = div({
      class: `prog-step${isActive ? " active" : ""}${isDone ? " done" : ""}`,
      onclick: () => { if (state.result) navigate(s.page); },
      title: s.label,
    },
      div({ class: "prog-dot", style: { background: isActive ? "var(--surface2)" : (isDone ? "var(--surface2)" : "var(--surface3)") } }, s.icon),
      div({ class: "prog-label" }, s.label),
    );
    bar.appendChild(stepEl);
  });
  return bar;
}

// ── PAGE RENDERER ────────────────────────────────────────────────
function renderPage() {
  const content = document.getElementById("page-content");
  if (!content) return;
  content.className = "page-content fade-in";

  const pages = {
    topics:   renderTopicsPage,
    ask:      renderAskPage,
    planner:  renderPlannerPage,
    explainer:renderExplainerPage,
    developer:renderDeveloperPage,
    critic:   renderCriticPage,
    final:    renderFinalPage,
  };

  content.innerHTML = "";
  const renderer = pages[state.page];
  if (renderer) renderer(content);
}

// ── PAGE: TOPICS ─────────────────────────────────────────────────
function renderTopicsPage(container) {
  const searchInput = input({
    type: "text",
    placeholder: "Search any topic… e.g. overfitting, LSTM, Apriori",
    oninput: (e) => filterTopics(e.target.value),
  });

  container.appendChild(
    div({ class: "topics-hero" },
      h1({}, "What do you want to learn today?"),
      p({}, "Pick any topic below — click it to ask a question. We cover everything in AI, Machine Learning, Deep Learning, and Data Mining."),
      div({ class: "topics-search" }, searchInput),
    )
  );

  Object.entries(DOMAINS).forEach(([domainName, domain]) => {
    const chipEls = domain.topics.map(topic =>
      div({
        class: "topic-chip",
        "data-topic": topic,
        onclick: () => {
          navigate("ask");
          setTimeout(() => {
            const ta = document.getElementById("ask-input");
            if (ta) { ta.value = `Explain ${topic}`; ta.focus(); }
          }, 50);
        }
      }, topic)
    );

    const section = div({ class: "domain-section" },
      div({ class: "domain-header" },
        span({ class: "domain-icon" }, domain.icon),
        div({ class: "domain-name", style: { color: domain.color } }, domainName),
        div({ class: "domain-count" }, `${domain.topics.length} topics`),
      ),
      div({ class: "topics-grid", id: `grid-${domainName.replace(/\s/g,"_")}` }, ...chipEls),
    );
    container.appendChild(section);
  });
}

function filterTopics(query) {
  const q = query.toLowerCase().trim();
  document.querySelectorAll(".topic-chip").forEach(chip => {
    const match = !q || chip.dataset.topic.toLowerCase().includes(q);
    chip.classList.toggle("hidden", !match);
  });
}

// ── PAGE: ASK ────────────────────────────────────────────────────
function renderAskPage(container) {
  const textarea = el("textarea", {
    class: "ask-textarea",
    id: "ask-input",
    placeholder: "Type your question here… e.g. What is gradient descent?",
    maxlength: "500",
  });

  if (state.question) textarea.value = state.question;

  const submitBtn = button({
    class: "ask-btn",
    onclick: () => handleAsk(textarea.value.trim()),
  }, "✦ Learn Now");

  const pills = EXAMPLE_QUESTIONS.map(q =>
    div({
      class: "example-pill",
      onclick: () => { textarea.value = q; textarea.focus(); }
    }, q)
  );

  container.appendChild(
    div({ class: "ask-hero" },
      h2({}, "Ask AgentTutor AI"),
      p({}, "Ask anything about AI, ML, Deep Learning, or Data Mining. The four agents will explain it step by step."),
    )
  );

  container.appendChild(
    div({ class: "ask-form" },
      textarea,
      div({}, submitBtn),
    )
  );

  container.appendChild(
    div({ class: "examples-section" },
      h3({}, "Try one of these"),
      div({ class: "example-pills" }, ...pills),
    )
  );
}

// ── LOADING PAGE ─────────────────────────────────────────────────
function renderLoadingPage(container) {
  const agents = [
    { name: "Planner Agent",   desc: "Understanding your question…" },
    { name: "Explainer Agent", desc: "Writing the theory explanation…" },
    { name: "Developer Agent", desc: "Preparing code example if needed…" },
    { name: "Critic Agent",    desc: "Reviewing and improving the answer…" },
  ];

  const items = agents.map((a, i) =>
    div({ class: "agent-load-item", id: `load-item-${i}` },
      div({ class: "agent-load-dot", id: `load-dot-${i}` }),
      div({ class: "agent-load-name" }, a.name),
      div({ class: "agent-load-status", id: `load-status-${i}` }, "waiting…"),
    )
  );

  container.innerHTML = "";
  container.appendChild(
    div({ class: "loading-wrap" },
      div({ class: "loading-title" }, "Thinking…"),
      p({ class: "loading-sub" }, `Processing: "${state.question}"`),
      div({ class: "agent-loading-list" }, ...items),
    )
  );

  // Animate agents sequentially
  let idx = 0;
  function tick() {
    if (idx > 0) {
      document.getElementById(`load-item-${idx-1}`)?.classList.replace("running","done");
      document.getElementById(`load-status-${idx-1}`).textContent = "done ✓";
    }
    if (idx < agents.length) {
      document.getElementById(`load-item-${idx}`)?.classList.add("running");
      document.getElementById(`load-status-${idx}`).textContent = agents[idx].desc;
      idx++;
      // Rough timing: planner ~5s, explainer ~15s, developer ~10s, critic ~15s
      const delays = [5000, 15000, 10000, 15000];
      setTimeout(tick, delays[idx-1] || 5000);
    }
  }
  tick();
}

async function handleAsk(question) {
  if (!question) { alert("Please type a question first."); return; }
  state.question = question;
  state.result = null;

  const content = document.getElementById("page-content");
  content.innerHTML = "";
  renderLoadingPage(content);
  updateNav();

  try {
    const res = await fetch("/api/pipeline", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ question }),
    });
    const data = await res.json();

    if (data.blocked) {
      content.innerHTML = `
        <div style="text-align:center;padding:60px 20px">
          <div style="font-size:48px;margin-bottom:16px">🚫</div>
          <h2 style="color:var(--text);margin-bottom:10px">Out of scope</h2>
          <p style="color:var(--text-dim);max-width:400px;margin:0 auto">${data.message}</p>
        </div>`;
      return;
    }

    state.result = data;
    buildLayout(); // Rebuild layout so pipeline nav items become enabled
    navigate("planner");

  } catch (err) {
    content.innerHTML = `
      <div style="text-align:center;padding:60px 20px">
        <div style="font-size:48px;margin-bottom:16px">⚠️</div>
        <h2 style="color:var(--danger);margin-bottom:10px">Connection error</h2>
        <p style="color:var(--text-dim)">Could not reach the backend. Make sure Ollama is running.<br><code style="font-size:12px;color:var(--developer)">python3 server.py</code></p>
      </div>`;
  }
}

// ── PAGE: PLANNER ─────────────────────────────────────────────────
function renderPlannerPage(container) {
  const r = state.result;
  if (!r) return;
  const meta = AGENT_META.planner;
  const p_data = r.planner;

  container.appendChild(buildProgressBar("planner"));

  // Agent header
  container.appendChild(
    div({ class: "agent-page-header" },
      div({ class: "agent-badge", style: { background: meta.bg } }, meta.icon),
      div({ class: "agent-page-meta" },
        div({ class: "agent-page-name", style: { color: meta.color } }, meta.label),
        div({ class: "agent-page-desc" }, meta.role),
        span({ class: "agent-role-pill", style: { background: meta.bg, color: meta.color } }, "Step 1 of 5"),
      )
    )
  );

  // What I found
  container.appendChild(
    div({ class: "card" },
      div({ class: "card-title" }, "What I Understood"),
      div({ class: "card-body" },
        div({ style: { marginBottom: "14px", fontSize: "15px", lineHeight: "1.8" } },
          p({}, `Your question is about: `),
          div({ style: { fontSize: "22px", fontWeight: "700", color: "var(--text)", margin: "6px 0 16px" } },
            span({ style: { color: meta.color } }, p_data.topic || "Unknown topic"),
          ),
        ),
        div({ class: "plan-meta-row" },
          metaChip(p_data.needs_theory, "📝 Theory"),
          metaChip(p_data.needs_example, "💡 Example"),
          metaChip(p_data.needs_code, "💻 Code"),
          metaChip(p_data.needs_review, "🔍 Review"),
        ),
        p({ style: { color: "var(--text-dim)", fontSize: "13px" } },
          qTypeFriendly(p_data.question_type)
        ),
      )
    )
  );

  // Learning steps
  if (p_data.learning_steps && p_data.learning_steps.length) {
    const stepEls = p_data.learning_steps.map((step, i) =>
      div({ class: "step-item" },
        div({ class: "step-num" }, String(i + 1)),
        div({ class: "step-text" }, step),
      )
    );
    container.appendChild(
      div({ class: "card" },
        div({ class: "card-title" }, "My Learning Plan"),
        div({ class: "card-body" },
          p({ style: { color: "var(--text-dim)", fontSize: "14px", marginBottom: "16px" } },
            "Here is the order I will use to explain this topic to you, step by step:"
          ),
          div({ class: "steps-list" }, ...stepEls),
        )
      )
    );
  }

  // Agents that will run
  container.appendChild(
    div({ class: "card" },
      div({ class: "card-title" }, "What Happens Next"),
      div({ class: "card-body" },
        p({ style: { color: "var(--text-dim)", fontSize: "14px", marginBottom: "16px" } },
          "These are the agents that will work together to answer your question:"
        ),
        div({ class: "agents-will-run" },
          willRunChip("📖 Explainer", "always", "var(--explainer)", "rgba(96,165,250,0.1)"),
          willRunChip("💻 Developer", p_data.needs_code ? "code requested" : "skipped", "var(--developer)", "rgba(52,211,153,0.1)", !p_data.needs_code),
          willRunChip("🔍 Critic",   "always", "var(--critic)", "rgba(251,191,36,0.1)"),
        )
      )
    )
  );

  container.appendChild(nextBtn("explainer", "See the Explanation →"));
}

function metaChip(active, label) {
  return div({ class: `meta-chip${active ? " active" : " inactive"}` },
    span({}, active ? "✅" : "⬜"),
    span({}, label),
  );
}

function willRunChip(label, reason, color, bg, skipped = false) {
  return div({ class: "will-run-chip", style: { color: skipped ? "var(--text-muted)" : color, background: skipped ? "var(--surface2)" : bg, borderColor: skipped ? "var(--border)" : color } },
    label + (reason ? ` · ${reason}` : "")
  );
}

function qTypeFriendly(qt) {
  const map = {
    concept_explanation: "This looks like a concept explanation question — I will focus on clear definitions and real-world analogies.",
    comparison: "This looks like a comparison question — I will highlight the key differences clearly.",
    how_to: "This looks like a how-to question — I will walk you through the steps.",
    example_request: "You asked for an example — I will make sure to include a clear practical example.",
  };
  return map[qt] || "I will explain this in a clear, beginner-friendly way.";
}

// ── PAGE: EXPLAINER ───────────────────────────────────────────────
function renderExplainerPage(container) {
  const r = state.result;
  if (!r) return;
  const meta = AGENT_META.explainer;
  const theory = r.critic.revised_theory || r.explainer.theory;

  container.appendChild(buildProgressBar("explainer"));

  container.appendChild(
    div({ class: "agent-page-header" },
      div({ class: "agent-badge", style: { background: meta.bg } }, meta.icon),
      div({ class: "agent-page-meta" },
        div({ class: "agent-page-name", style: { color: meta.color } }, meta.label),
        div({ class: "agent-page-desc" }, meta.role),
        span({ class: "agent-role-pill", style: { background: meta.bg, color: meta.color } }, "Step 2 of 5"),
      )
    )
  );

  // Section 1: Simple Explanation
  if (theory) {
    const card1 = div({ class: "card" },
      div({ class: "card-title" }, "🧠 1. Simple Explanation"),
      div({ class: "card-body theory-text" }),
    );
    container.appendChild(card1);
    card1.querySelector(".theory-text").innerHTML = renderMarkdown(theory);
  }

  // Section 2: Why It Matters
  if (r.explainer.why_it_matters) {
    const card2 = div({ class: "card" },
      div({ class: "card-title" }, "🎯 2. Why It Matters"),
      div({ class: "card-body theory-text" }),
    );
    container.appendChild(card2);
    card2.querySelector(".theory-text").innerHTML = renderMarkdown(r.explainer.why_it_matters);
  }

  // Section 3: Intuition / Example
  if (r.explainer.intuition_example) {
    const card3 = div({ class: "card" },
      div({ class: "card-title" }, "🔍 3. Intuition / Example"),
      div({ class: "card-body theory-text" }),
    );
    container.appendChild(card3);
    card3.querySelector(".theory-text").innerHTML = renderMarkdown(r.explainer.intuition_example);
  }

  if (r.critic.revision_needed) {
    container.appendChild(
      div({ style: { fontSize: "12px", color: "var(--text-muted)", marginTop: "-8px", marginBottom: "16px", padding: "8px 12px", background: "var(--surface)", border: "1px solid var(--border)", borderRadius: "8px" } },
        "✦ This explanation was improved by the Critic Agent for better clarity."
      )
    );
  }

  container.appendChild(nextBtn("developer", "See the Code →"));
}

// ── PAGE: DEVELOPER ───────────────────────────────────────────────
function renderDeveloperPage(container) {
  const r = state.result;
  if (!r) return;
  const meta = AGENT_META.developer;
  const dev = r.developer;

  container.appendChild(buildProgressBar("developer"));

  container.appendChild(
    div({ class: "agent-page-header" },
      div({ class: "agent-badge", style: { background: meta.bg } }, meta.icon),
      div({ class: "agent-page-meta" },
        div({ class: "agent-page-name", style: { color: meta.color } }, meta.label),
        div({ class: "agent-page-desc" }, meta.role),
        span({ class: "agent-role-pill", style: { background: meta.bg, color: meta.color } }, "Step 3 of 5"),
      )
    )
  );

  if (dev.skipped || !dev.code) {
    container.appendChild(
      div({ class: "skipped-box" },
        div({ class: "skipped-icon" }, "💡"),
        div({ class: "skipped-title" }, "No Code Needed Here"),
        div({ class: "skipped-desc" },
          `The Planner Agent decided that "${r.planner.topic}" is best understood through a clear explanation and analogy, without needing a code example. Code would not make it clearer — words work better for this concept.`
        )
      )
    );
  } else {
    // Section 4: Code Example
    const codeCard = div({ class: "card" },
      div({ class: "card-title" }, "⚙️ 4. Code Example"),
      div({ class: "card-body" },
        p({ style: { fontSize: "14px", color: "var(--text-dim)", marginBottom: "16px" } },
          dev.purpose || `A simple Python example to help you understand ${r.planner.topic}.`
        ),
      )
    );
    container.appendChild(codeCard);

    const codeWrap = div({ class: "code-block-wrap" });
    codeWrap.innerHTML = buildCodeBlockHTML("python", dev.code, highlightPython(dev.code));
    codeCard.querySelector(".card-body").appendChild(codeWrap);

    // Section 5: Code Explanation
    const explanationText = dev.code_explanation;
    if (explanationText) {
      const explCard = div({ class: "card" },
        div({ class: "card-title" }, "🔍 5. Code Explanation"),
        div({ class: "card-body theory-text" }),
      );
      container.appendChild(explCard);
      explCard.querySelector(".theory-text").innerHTML = renderMarkdown(explanationText);
    } else {
      container.appendChild(
        div({ class: "card" },
          div({ class: "card-title" }, "🔍 5. Code Explanation"),
          div({ class: "card-body" },
            p({},
              "Read the code from top to bottom — each line has an inline comment. " +
              "Variable names are kept descriptive so you can follow the logic easily. " +
              "Copy it into any Python environment and run it to see the output."
            )
          )
        )
      );
    }
  }

  container.appendChild(nextBtn("critic", "See the Review →"));
}

// ── PAGE: CRITIC ──────────────────────────────────────────────────
function renderCriticPage(container) {
  const r = state.result;
  if (!r) return;
  const meta = AGENT_META.critic;
  const c = r.critic;

  container.appendChild(buildProgressBar("critic"));

  container.appendChild(
    div({ class: "agent-page-header" },
      div({ class: "agent-badge", style: { background: meta.bg } }, meta.icon),
      div({ class: "agent-page-meta" },
        div({ class: "agent-page-name", style: { color: meta.color } }, meta.label),
        div({ class: "agent-page-desc" }, meta.role),
        span({ class: "agent-role-pill", style: { background: meta.bg, color: meta.color } }, "Step 4 of 5"),
      )
    )
  );

  // Clarity check
  const clarityGood = c.clarity_check === "good";
  container.appendChild(
    div({ class: "card" },
      div({ class: "card-title" }, "Clarity Check"),
      div({ class: "card-body" },
        div({ class: `clarity-badge ${c.clarity_check || "good"}` },
          span({}, clarityGood ? "✅" : "⚠️"),
          span({}, clarityGood ? "Explanation is clear and easy to understand!" : "Explanation needed some improvement."),
        ),
        p({ style: { fontSize: "14px", color: "var(--text-dim)", lineHeight: "1.7" } },
          clarityGood
            ? "The Critic Agent reviewed the explanation and found it to be accurate, student-friendly, and well-structured. No major changes were needed."
            : "The Critic Agent noticed that the explanation could be clearer. It has been improved and the better version is shown on the Explainer page."
        )
      )
    )
  );

  // Code feedback
  if (c.code_feedback && c.code_feedback !== "n/a") {
    container.appendChild(
      div({ class: "card" },
        div({ class: "card-title" }, "Code Feedback"),
        div({ class: "card-body" },
          p({ style: { fontSize: "15px", lineHeight: "1.8" } }, c.code_feedback)
        )
      )
    );
  }

  // Section 6: Key Points / Common Mistakes (only from key_points — never mix with missing_points)
  if (c.key_points && c.key_points.length > 0) {
    const pointEls = c.key_points.map(pt =>
      div({ class: "missing-point" },
        span({ class: "missing-point-icon" }, "⚠️"),
        span({}, pt),
      )
    );
    container.appendChild(
      div({ class: "card" },
        div({ class: "card-title" }, "⚠️ 6. Key Points / Common Mistakes"),
        div({ class: "card-body" },
          p({ style: { fontSize: "14px", color: "var(--text-dim)", marginBottom: "14px" } },
            "Important notes and common mistakes students make about this topic:"
          ),
          ...pointEls,
        )
      )
    );
  }

  // Also Worth Knowing (missing_points — separate from key_points)
  if (c.missing_points && c.missing_points.length > 0) {
    const extraEls = c.missing_points.map(pt =>
      div({ class: "missing-point" },
        span({ class: "missing-point-icon" }, "💡"),
        span({}, pt),
      )
    );
    container.appendChild(
      div({ class: "card" },
        div({ class: "card-title" }, "💡 Also Worth Knowing"),
        div({ class: "card-body" },
          p({ style: { fontSize: "14px", color: "var(--text-dim)", marginBottom: "14px" } },
            "The Critic Agent suggests looking into these related ideas to deepen your understanding:"
          ),
          ...extraEls,
        )
      )
    );
  }

  // Revised theory note
  if (c.revision_needed && c.revised_theory) {
    container.appendChild(
      div({ class: "revision-block" },
        div({ class: "revision-label" }, "✦ Revision Applied"),
        p({ style: { fontSize: "14px", color: "var(--text-dim)", lineHeight: "1.7" } },
          "The Critic found parts of the original explanation that could be clearer. A revised version was written and is shown in the Explainer page."
        )
      )
    );
  }

  container.appendChild(nextBtn("final", "See the Final Answer →"));
}

// ── PAGE: FINAL ───────────────────────────────────────────────────
function renderFinalPage(container) {
  const r = state.result;
  if (!r) return;
  const meta = AGENT_META.final;
  const p_data = r.planner;
  const theory = r.critic.revised_theory || r.explainer.theory;

  container.appendChild(buildProgressBar("final"));

  container.appendChild(
    div({ class: "agent-page-header" },
      div({ class: "agent-badge", style: { background: meta.bg } }, meta.icon),
      div({ class: "agent-page-meta" },
        div({ class: "agent-page-name", style: { color: meta.color } }, meta.label),
        div({ class: "agent-page-desc" }, "Everything combined into one clean, easy-to-read answer."),
        span({ class: "agent-role-pill", style: { background: meta.bg, color: meta.color } }, "Step 5 of 5 · Complete"),
      )
    )
  );

  const finalWrap = div({ class: "final-answer-wrap" });

  // Banner
  finalWrap.appendChild(
    div({ class: "final-banner" },
      div({ class: "final-banner-icon" }, "🎓"),
      div({},
        div({ class: "final-banner-title" }, p_data.topic || "Your Answer"),
        div({ class: "final-banner-sub" }, `Answer to: "${state.question}"`),
      )
    )
  );

  const body = div({ class: "final-body" });

  // Section 1: Simple Explanation
  if (theory) {
    const s1 = div({ class: "final-section" });
    s1.appendChild(div({ class: "final-section-title" }, "🧠 1. Simple Explanation"));
    const d1 = div({ class: "theory-text" });
    d1.innerHTML = renderMarkdown(theory);
    s1.appendChild(d1);
    body.appendChild(s1);
  }

  // Section 2: Why It Matters
  if (r.explainer.why_it_matters) {
    const s2 = div({ class: "final-section" });
    s2.appendChild(div({ class: "final-section-title" }, "🎯 2. Why It Matters"));
    const d2 = div({ class: "theory-text" });
    d2.innerHTML = renderMarkdown(r.explainer.why_it_matters);
    s2.appendChild(d2);
    body.appendChild(s2);
  }

  // Section 3: Intuition / Example
  if (r.explainer.intuition_example) {
    const s3 = div({ class: "final-section" });
    s3.appendChild(div({ class: "final-section-title" }, "🔍 3. Intuition / Example"));
    const d3 = div({ class: "theory-text" });
    d3.innerHTML = renderMarkdown(r.explainer.intuition_example);
    s3.appendChild(d3);
    body.appendChild(s3);
  }

  // Section 4: Code Example
  if (r.developer.code && !r.developer.skipped) {
    const s4 = div({ class: "final-section" });
    s4.appendChild(div({ class: "final-section-title" }, "⚙️ 4. Code Example"));
    s4.appendChild(
      p({ style: { fontSize: "14px", color: "var(--text-dim)", marginBottom: "14px" } },
        r.developer.purpose || "A simple Python example to illustrate the concept."
      )
    );
    const codeWrap = div({ class: "code-block-wrap" });
    codeWrap.innerHTML = buildCodeBlockHTML("python", r.developer.code, highlightPython(r.developer.code));
    s4.appendChild(codeWrap);
    body.appendChild(s4);
  }

  // Section 5: Code Explanation
  if (r.developer.code && !r.developer.skipped && r.developer.code_explanation) {
    const s5 = div({ class: "final-section" });
    s5.appendChild(div({ class: "final-section-title" }, "🔍 5. Code Explanation"));
    const d5 = div({ class: "theory-text" });
    d5.innerHTML = renderMarkdown(r.developer.code_explanation);
    s5.appendChild(d5);
    body.appendChild(s5);
  }

  // Section 6: Key Points / Common Mistakes (key_points only — not missing_points)
  if (r.critic.key_points && r.critic.key_points.length > 0) {
    const s6 = div({ class: "final-section" });
    s6.appendChild(div({ class: "final-section-title" }, "⚠️ 6. Key Points / Common Mistakes"));
    r.critic.key_points.forEach(pt => {
      s6.appendChild(
        div({ class: "missing-point" },
          span({ class: "missing-point-icon" }, "⚠️"),
          span({ style: { fontSize: "14px" } }, pt),
        )
      );
    });
    body.appendChild(s6);
  }

  // Also Worth Knowing (missing_points — separate card, not section 6)
  if (r.critic.missing_points && r.critic.missing_points.length > 0) {
    const sExtra = div({ class: "final-section" });
    sExtra.appendChild(div({ class: "final-section-title" }, "💡 Also Worth Knowing"));
    r.critic.missing_points.forEach(pt => {
      sExtra.appendChild(
        div({ class: "missing-point" },
          span({ class: "missing-point-icon" }, "💡"),
          span({ style: { fontSize: "14px" } }, pt),
        )
      );
    });
    body.appendChild(sExtra);
  }

  // Section 7: Final Takeaway
  body.appendChild(
    div({ class: "final-section" },
      div({ class: "final-section-title" }, "✅ 7. Final Takeaway"),
      div({ class: "takeaway-box" },
        div({ class: "icon" }, "🎯"),
        p({},
          `**${p_data.topic}** is an important concept in AI, ML, Deep Learning, and Data Mining. ` +
          `Understanding it well will help you build better models and think more clearly about data. ` +
          `Keep exploring — every concept builds on the one before.`
        ),
      )
    )
  );

  finalWrap.appendChild(body);
  container.appendChild(finalWrap);

  // Ask another question button
  container.appendChild(
    div({ style: { marginTop: "24px", display: "flex", gap: "12px" } },
      button({
        class: "ask-btn",
        style: { background: "var(--surface2)", border: "1px solid var(--border)" },
        onclick: () => { state.question = ""; state.result = null; buildLayout(); navigate("ask"); }
      }, "← Ask Another Question"),
      button({
        class: "ask-btn",
        style: { background: "var(--surface2)", border: "1px solid var(--border)" },
        onclick: () => { buildLayout(); navigate("topics"); }
      }, "📚 Explore Topics"),
    )
  );
}

// ── HELPER: Next Button ───────────────────────────────────────────
function nextBtn(targetPage, label) {
  return div({ style: { marginTop: "24px" } },
    button({
      class: "ask-btn",
      onclick: () => navigate(targetPage),
    }, label)
  );
}

// ── INIT ──────────────────────────────────────────────────────────
buildLayout();
navigate("topics");
