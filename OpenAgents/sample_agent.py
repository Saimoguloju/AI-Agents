"""
OpenAgents — Sample Agent: a persistent network (MCP tools + A2A handoffs)
==========================================================================
Signature feature: agents live in a persistent NETWORK. They use TOOLS via MCP
(vertical: agent -> tool) and collaborate via A2A (horizontal: agent -> agent),
discovering each other by advertised capability.

CONCEPTUAL & self-contained — a tiny Network mimics MCP + A2A. No API key, no install.

Run:  python sample_agent.py
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Callable


# --- MCP: a tool server an agent can call ---------------------------------
class MCPServer:
    def __init__(self):
        self.tools: dict[str, Callable] = {
            "search_sources": lambda q: ["paper-A: agents", "paper-B: RAG"],
        }

    def call(self, tool: str, arg):
        return self.tools[tool](arg)


# --- An agent advertises capabilities and can hand off (A2A) --------------
@dataclass
class Agent:
    name: str
    capability: str                       # what this agent advertises via A2A
    network: "Network" = field(default=None)

    def handle(self, message: str) -> str:
        if self.capability == "research":
            sources = self.network.mcp.call("search_sources", message)
            print(f"  [{self.name}] MCP search_sources -> {sources}")
            # A2A handoff: discover an analyst and pass the work along
            analyst = self.network.discover("analysis")
            print(f"  [{self.name}] A2A handoff -> {analyst.name}")
            return analyst.handle(str(sources))
        if self.capability == "analysis":
            return f"Analysis: found {len(eval(message))} sources; theme = agentic systems."
        return "unhandled"


# --- Persistent network: registry + shared MCP ----------------------------
class Network:
    def __init__(self):
        self.agents: list[Agent] = []
        self.mcp = MCPServer()

    def add(self, agent: Agent):
        agent.network = self
        self.agents.append(agent)
        return agent

    def discover(self, capability: str) -> Agent:
        return next(a for a in self.agents if a.capability == capability)

    def ask(self, capability: str, message: str) -> str:
        return self.discover(capability).handle(message)


if __name__ == "__main__":
    net = Network()
    net.add(Agent("Researcher", "research"))
    net.add(Agent("Analyst", "analysis"))
    print("TASK: research the 2026 AI-agent landscape\n")
    print("\nRESULT:", net.ask("research", "2026 AI agents"))

# --- Real version ---------------------------------------------------------
# pip install openagents
# OpenAgents centers on launching a persistent network where agents register,
# expose capabilities over A2A, and consume tools over MCP. See the project's
# network/launcher config for spinning up real distributed agents.
