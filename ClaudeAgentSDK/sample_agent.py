"""
Claude Agent SDK — Sample Agent: "give Claude a computer"
=========================================================
Signature feature: you describe a GOAL and register TOOLS; the SDK owns the
agent loop (plan -> call tool -> observe -> iterate) and context management.
You do NOT hand-write the think/act/observe loop.

CONCEPTUAL & self-contained — a tiny loop stands in for the SDK-managed loop,
with a mock Claude. No API key, no `pip install claude-agent-sdk`.

Run:  python sample_agent.py
"""
from __future__ import annotations
import os
from dataclasses import dataclass, field
from typing import Callable


# --- Tools the agent is allowed to use ------------------------------------
def list_files(_: str = "") -> str:
    return "report.txt, data.csv, notes.md"

def read_file(name: str) -> str:
    return {"report.txt": "Q2 revenue grew 12%."}.get(name, "<empty>")


@dataclass
class Tool:
    name: str
    description: str
    fn: Callable[[str], str]


# --- Mock Claude: emits tool calls, then a final answer -------------------
class MockClaude:
    """Returns either a tool call or a final answer, based on what it has seen."""
    def step(self, goal: str, observations: list[str]):
        seen = " ".join(observations)
        if "report.txt" not in seen:
            return {"type": "tool_use", "name": "list_files", "input": ""}
        if "revenue" not in seen:
            return {"type": "tool_use", "name": "read_file", "input": "report.txt"}
        return {"type": "text", "text": "Summary: Q2 revenue grew 12% (from report.txt)."}


# --- The SDK-managed agent: YOU just give a goal + tools ------------------
@dataclass
class ClaudeAgent:
    tools: dict[str, Tool]
    model: MockClaude = field(default_factory=MockClaude)

    def query(self, goal: str, max_turns: int = 6) -> str:
        print(f"GOAL: {goal}\n")
        observations: list[str] = []
        for turn in range(1, max_turns + 1):
            action = self.model.step(goal, observations)
            if action["type"] == "text":
                print(f"[turn {turn}] final answer")
                return action["text"]
            tool = self.tools[action["name"]]
            result = tool.fn(action["input"])
            print(f"[turn {turn}] tool {tool.name}({action['input']!r}) -> {result}")
            observations.append(result)
        return "stopped: max turns reached"


def build_agent() -> ClaudeAgent:
    tools = {
        "list_files": Tool("list_files", "List files in the workspace", list_files),
        "read_file": Tool("read_file", "Read a file by name", read_file),
    }
    return ClaudeAgent(tools=tools)


if __name__ == "__main__":
    if not os.getenv("ANTHROPIC_API_KEY"):
        print("(no ANTHROPIC_API_KEY found — running the offline mock)\n")
    agent = build_agent()
    print("\nRESULT:", agent.query("Summarize the contents of report.txt."))

# --- Real version ---------------------------------------------------------
# pip install claude-agent-sdk        (needs ANTHROPIC_API_KEY)
# from claude_agent_sdk import query, ClaudeAgentOptions
# async for msg in query(prompt="Summarize report.txt",
#                        options=ClaudeAgentOptions(allowed_tools=["Read", "Bash"])):
#     print(msg)   # the SDK runs the full loop, tool execution, and compaction
