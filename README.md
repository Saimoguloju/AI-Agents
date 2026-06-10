# AI Agents

> Hands-on exploration of autonomous AI agent systems — from fundamentals to multi-agent architectures.

**Repository:** [github.com/Saimoguloju/AI-Agents](https://github.com/Saimoguloju/AI-Agents)

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
│   ── Core frameworks ──
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
│   ── More frameworks ──
├── GoogleADK/
│   └── google_adk.ipynb         # Code-first, multi-language agents (Google/Gemini)
├── SemanticKernel/
│   └── semantic_kernel.ipynb    # Plugins + planners for .NET/enterprise (Microsoft)
├── LlamaIndex/
│   └── llamaindex.ipynb         # Agentic RAG & document agents
├── Smolagents/
│   └── smolagents.ipynb         # Minimal "agents that think in code" (Hugging Face)
├── MetaGPT/
│   └── metagpt.ipynb            # SOP-driven AI software company
├── OpenAgents/
│   └── openagents.ipynb         # Persistent agent networks (MCP + A2A)
├── VercelAISDK/
│   └── vercel_ai_sdk.ipynb      # TypeScript AI for the web (Vercel)
├── Mastra/
│   └── mastra.ipynb             # Full TypeScript agent stack
├── Mirascope/
│   └── mirascope.ipynb          # The LLM "anti-framework" (Goldilocks API)
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
| **Google ADK** | `google_adk.ipynb` | Code-first, multi-language (Py/TS/Go/Java), Gemini-optimized |
| **Semantic Kernel** | `semantic_kernel.ipynb` | Plugins + planners + memory; .NET/Azure enterprise |
| **LlamaIndex** | `llamaindex.ipynb` | Agentic RAG, advanced retrieval, document agents |
| **smolagents** | `smolagents.ipynb` | Minimalist agents that act by writing code (Hugging Face) |
| **MetaGPT** | `metagpt.ipynb` | `Code = SOP(Team)` — simulated software company |
| **OpenAgents** | `openagents.ipynb` | Persistent agent networks; native MCP + A2A |
| **Vercel AI SDK** | `vercel_ai_sdk.ipynb` | TypeScript-first AI for Next.js/web; unified providers |
| **Mastra** | `mastra.ipynb` | Full TypeScript agent stack (workflows, RAG, memory, evals) |
| **Mirascope** | `mirascope.ipynb` | "Anti-framework" — raw-API control with framework ergonomics |

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
git clone https://github.com/Saimoguloju/AI-Agents.git
cd AI-Agents

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

## Sample Agents

Each framework folder also contains a **runnable sample agent** that demonstrates
that framework's signature pattern. These are **conceptual and self-contained**:
they use a tiny built-in mock LLM, so they run with **no API key and no framework
install** — handy for seeing the core idea before wiring up the real SDK.

```bash
# Python samples (no dependencies beyond the standard library)
python Basics/sample_agent.py            # raw ReAct loop (Reason -> Act -> Observe)
python LangGraph/sample_agent.py         # stateful graph + conditional routing
python CrewAI/sample_agent.py            # role/goal/backstory crew, sequential
python AutoGen/sample_agent.py           # round-robin conversational team
python PydanticAI/sample_agent.py        # typed output + validation self-correction
python ClaudeAgentSDK/sample_agent.py    # SDK-managed tool-use loop
python OpenAIAgentsSDK/sample_agent.py   # triage agent: tools, handoffs, guardrails
python GoogleADK/sample_agent.py         # LLM agents + sequential workflow agent
python SemanticKernel/sample_agent.py    # kernel + plugins + planner
python LlamaIndex/sample_agent.py        # agentic RAG (decide WHEN to retrieve)
python Smolagents/sample_agent.py        # CodeAgent that acts by writing code
python MetaGPT/sample_agent.py           # SOP role pipeline (Code = SOP(Team))
python OpenAgents/sample_agent.py        # persistent network: MCP tools + A2A handoff
python Mirascope/sample_agent.py         # decorated function IS the LLM call

# TypeScript samples (TS-only frameworks) — run with tsx
npx tsx VercelAISDK/sample_agent.ts      # unified provider + tool-calling loop
npx tsx Mastra/sample_agent.ts           # agent + tools + persistent memory
```

> Each sample ends with a commented **"Real version"** block showing the
> equivalent code using the actual framework (with the `pip install` / `npm install`
> and API-key requirements).

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
