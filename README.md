# AI Agents

> Hands-on exploration of autonomous AI agent systems — from fundamentals to multi-agent architectures.

---

## What This Repository Is

A structured learning and experimentation space for building modern AI agents. Each notebook covers a specific concept with working code, diagrams, and explanations grounded in current research and industry practice (2026).

---

## Project Structure

```
AI Agents/
│
├── Basics/
│   └── intro.ipynb          # What are AI agents, how they work, future outlook
│
├── requirements.txt         # Python dependencies
├── .gitignore
└── README.md
```

> More modules (Tools, Memory, Planning, Multi-Agent) will be added progressively.

---

## Topics Covered

| Module | Notebook | Description |
|---|---|---|
| **Basics** | `intro.ipynb` | AI agents overview, architecture, types, future |
| **Tools** | *(coming soon)* | Connecting agents to web search, APIs, code execution |
| **Memory** | *(coming soon)* | Short-term context, long-term vector stores, RAG |
| **Planning** | *(coming soon)* | ReAct, Plan-Execute, Tree of Thoughts |
| **Multi-Agent** | *(coming soon)* | Orchestrator + specialist agent patterns |

---

## Core Concepts

- **Planning** — How agents decompose complex goals into executable sub-tasks
- **Memory** — Short-term (in-context) and long-term (vector stores) memory systems
- **Tool Use** — Connecting LLMs to web search, code runners, file systems, and APIs
- **ReAct Loop** — Reason → Act → Observe → Repeat until goal is achieved
- **Multi-Agent Systems** — Orchestrating multiple specialized agents to collaborate

---

## Setup

### Prerequisites

- Python 3.11+
- Jupyter (via `ipykernel`)

### Install

```bash
# Clone the repo
git clone <repo-url>
cd "AI Agents"

# Create and activate virtual environment
python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # macOS/Linux

# Install dependencies
pip install -r requirements.txt
```

### Run

```bash
jupyter notebook
```

Open any `.ipynb` file from the browser interface.

---

## Dependencies

| Package | Purpose |
|---|---|
| `ipykernel` | Jupyter notebook kernel for Python |

More packages will be added as agent modules are built (e.g., `anthropic`, `langchain`, `chromadb`).

---

## Goals

- Build AI agents from scratch to understand every component deeply
- Experiment with different planning and memory strategies
- Implement multi-agent collaboration patterns
- Document findings clearly for reference and learning

---

## Resources

- [Anthropic Claude API Docs](https://docs.anthropic.com)
- [LangChain Documentation](https://python.langchain.com)
- [ReAct Paper — Yao et al. 2022](https://arxiv.org/abs/2210.03629)
- [IBM Guide to AI Agents](https://www.ibm.com/think/ai-agents)
- [Google Cloud AI Agent Trends 2026](https://cloud.google.com/resources/content/ai-agent-trends-2026)
