"""
AutoGen — Sample Agent: conversational multi-agent team
=======================================================
Signature feature: agents that solve problems by TALKING TO EACH OTHER in
turns (round-robin), until a termination condition is met.

CONCEPTUAL & self-contained — a tiny engine mimics AutoGen's AssistantAgent +
RoundRobinGroupChat. No API key, no `pip install autogen-agentchat`.

Run:  python sample_agent.py
"""
from __future__ import annotations
from dataclasses import dataclass


# --- Mock model client: replies based on the agent's system role ----------
def mock_client(system: str, conversation: list[str]) -> str:
    last = conversation[-1] if conversation else ""
    if "Coder" in system:
        return ("Here is a function:\n"
                "def is_even(n): return n % 2 == 0")
    if "Reviewer" in system:
        if "is_even" in last:
            return "Looks correct and handles negatives. APPROVE. TERMINATE"
        return "Please share the code so I can review it."
    return "..."


# --- AutoGen-style agent --------------------------------------------------
@dataclass
class AssistantAgent:
    name: str
    system_message: str

    def respond(self, conversation: list[str]) -> str:
        return mock_client(self.system_message, conversation)


# --- RoundRobinGroupChat: agents take turns until TERMINATE ---------------
class RoundRobinGroupChat:
    def __init__(self, agents: list[AssistantAgent], termination_text="TERMINATE", max_turns=8):
        self.agents, self.term, self.max_turns = agents, termination_text, max_turns

    def run(self, task: str) -> list[str]:
        convo = [f"user: {task}"]
        print(f"user: {task}")
        turn = 0
        while turn < self.max_turns:
            agent = self.agents[turn % len(self.agents)]
            reply = agent.respond(convo)
            line = f"{agent.name}: {reply}"
            print(line)
            convo.append(line)
            if self.term in reply:
                break
            turn += 1
        return convo


coder = AssistantAgent("coder", "You are a Coder. Write Python to satisfy the task.")
reviewer = AssistantAgent("reviewer", "You are a Reviewer. Approve correct code, else ask for it. Say TERMINATE when done.")

team = RoundRobinGroupChat([coder, reviewer])

if __name__ == "__main__":
    team.run("Write a Python function that checks if a number is even.")

# --- Real version ---------------------------------------------------------
# pip install -U "autogen-agentchat" "autogen-ext[openai]"
# from autogen_agentchat.agents import AssistantAgent
# from autogen_agentchat.teams import RoundRobinGroupChat
# from autogen_agentchat.conditions import TextMentionTermination
# from autogen_ext.models.openai import OpenAIChatCompletionClient
# team = RoundRobinGroupChat([coder, reviewer],
#                            termination_condition=TextMentionTermination("TERMINATE"))
# await team.run(task="...")
