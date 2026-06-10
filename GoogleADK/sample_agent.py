"""
Google ADK — Sample Agent: LLM agents orchestrated by a workflow agent
======================================================================
Signature feature: code-first agents. LLM agents are the "brains"; WORKFLOW
agents (Sequential / Parallel / Loop) deterministically orchestrate them, and a
Runner manages session state + events.

CONCEPTUAL & self-contained — a tiny engine mimics ADK's LlmAgent +
SequentialAgent + Runner. No API key, no `pip install google-adk`.

Run:  python sample_agent.py
"""
from __future__ import annotations
from dataclasses import dataclass, field


# --- Mock model -----------------------------------------------------------
def mock_model(instruction: str, state: dict) -> str:
    if "outline" in instruction.lower():
        return "1) what are agents 2) frameworks 3) the future"
    if "draft" in instruction.lower():
        return f"Draft based on outline [{state.get('outline','')}]: Agents are autonomous LLM systems..."
    if "polish" in instruction.lower():
        return f"Polished: {state.get('draft','')[:60]}... (tightened & proofed)"
    return "..."


# --- LlmAgent: a brain that reads/writes shared session state -------------
@dataclass
class LlmAgent:
    name: str
    instruction: str
    output_key: str             # where its result lands in session state

    def run(self, state: dict) -> None:
        result = mock_model(self.instruction, state)
        state[self.output_key] = result
        print(f"  [{self.name}] -> {self.output_key} = {result}")


# --- SequentialAgent: an assembly line ------------------------------------
@dataclass
class SequentialAgent:
    name: str
    sub_agents: list[LlmAgent] = field(default_factory=list)

    def run(self, state: dict) -> None:
        print(f"[workflow {self.name}] running {len(self.sub_agents)} agents in sequence")
        for a in self.sub_agents:
            a.run(state)


# --- Runner: owns session state + drives the root agent -------------------
class Runner:
    def run(self, agent, user_msg: str) -> dict:
        print(f"USER: {user_msg}\n")
        state = {"request": user_msg}
        agent.run(state)
        return state


pipeline = SequentialAgent(
    name="BlogPipeline",
    sub_agents=[
        LlmAgent("Outliner", "Create an outline for the topic", "outline"),
        LlmAgent("Writer", "Write a draft from the outline", "draft"),
        LlmAgent("Editor", "Polish the draft", "final"),
    ],
)

if __name__ == "__main__":
    final_state = Runner().run(pipeline, "Write a short post on the 2026 AI agent landscape.")
    print("\nFINAL:", final_state["final"])

# --- Real version ---------------------------------------------------------
# pip install google-adk             (needs a Gemini/GOOGLE_API_KEY)
# from google.adk.agents import LlmAgent, SequentialAgent
# from google.adk.runners import Runner
# pipeline = SequentialAgent(name="...", sub_agents=[LlmAgent(model="gemini-2.0-flash", ...)])
