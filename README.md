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
│   └── intro.ipynb              # What are AI agents, how they work, future outlook
│
├── LangGraph/
│   └── langgraph.ipynb          # Stateful graph orchestration (LangChain stack)
├── CrewAI/
│   └── crewai.ipynb             # Role-playing multi-agent teams
├── AutoGen/
│   └── autogen.ipynb            # Conversational multi-agent systems (Microsoft)
├── PydanticAI/
│   └── pydantic_ai.ipynb        # Type-safe, structured-output agents
├── ClaudeAgentSDK/
│   └── claude_agent_sdk.ipynb   # "Give Claude a computer" (Anthropic)
├── OpenAIAgentsSDK/
│   └── openai_agents_sdk.ipynb  # Lightweight handoffs + guardrails (OpenAI)
│
├── requirements.txt             # Python dependencies
├── .gitignore
└── README.md
```

> More conceptual modules (Tools, Memory, Planning) will be added progressively.

---

## Topics Covered

| Module | Notebook | Description |
|---|---|---|
| **Basics** | `intro.ipynb` | AI agents overview, architecture, types, future |
| **LangGraph** | `langgraph.ipynb` | Graph-based, durable, stateful agent orchestration |
| **CrewAI** | `crewai.ipynb` | Role/goal/backstory multi-agent teams (Crews & Flows) |
| **AutoGen** | `autogen.ipynb` | Async, actor-model conversational agents → MS Agent Framework |
| **Pydantic AI** | `pydantic_ai.ipynb` | Type safety + guaranteed structured output |
| **Claude Agent SDK** | `claude_agent_sdk.ipynb` | Model-native agent loop, tools, context management |
| **OpenAI Agents SDK** | `openai_agents_sdk.ipynb` | Four primitives: agents, tools, handoffs, guardrails |

> Each framework notebook follows the same structure: **what it is → how it works → architecture → conceptual code → how it's advanced vs other frameworks → when to use it**, with sourced links to current (2026) documentation.

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
