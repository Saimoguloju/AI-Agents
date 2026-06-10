"""
CrewAI — Sample Agent: role-playing agents collaborating as a crew
==================================================================
Signature feature: agents defined by ROLE + GOAL + BACKSTORY, each assigned a
TASK, run by a CREW with a sequential process (one agent's output feeds the next).

CONCEPTUAL & self-contained — a tiny engine mimics CrewAI's Agent/Task/Crew API.
No API key, no `pip install crewai`.

Run:  python sample_agent.py
"""
from __future__ import annotations
from dataclasses import dataclass, field


# --- Mock LLM: role-aware so each agent "sounds" different -----------------
def mock_llm(role: str, prompt: str) -> str:
    if "Researcher" in role:
        return ("Findings: AI agents in 2026 are shifting from demos to "
                "production; key themes are reliability, memory, and multi-agent orchestration.")
    if "Writer" in role:
        return ("Blog post: 'From Demos to Production' — 2026 is the year AI "
                "agents grow up. Teams now prize reliability, durable memory, and "
                "coordinated multi-agent systems over flashy one-offs.")
    if "Editor" in role:
        # Edit only the incoming draft, not the whole prompt preamble.
        draft = prompt.split("Blog post:", 1)[-1].strip() if "Blog post:" in prompt else prompt
        return "FINAL (edited): " + " ".join(draft.split())
    return "..."


# --- CrewAI-style primitives ----------------------------------------------
@dataclass
class Agent:
    role: str
    goal: str
    backstory: str  # the backstory steers tone/behavior of the role

    def execute(self, task_description: str, context: str = "") -> str:
        prompt = f"{self.backstory}\nGoal: {self.goal}\nTask: {task_description}\n{context}"
        return mock_llm(self.role, prompt)


@dataclass
class Task:
    description: str
    agent: Agent
    expected_output: str


@dataclass
class Crew:
    agents: list[Agent]
    tasks: list[Task]
    process: str = "sequential"
    _log: list[str] = field(default_factory=list)

    def kickoff(self) -> str:
        context = ""
        for task in self.tasks:
            print(f">>> {task.agent.role} working on: {task.description}")
            result = task.agent.execute(task.description, context)
            print(f"    -> {result}\n")
            context = result  # sequential: output becomes next task's context
        return context


# --- Define the crew ------------------------------------------------------
researcher = Agent(
    role="Senior Researcher",
    goal="Uncover the key 2026 AI-agent trends",
    backstory="You are a meticulous analyst who values primary sources.",
)
writer = Agent(
    role="Tech Writer",
    goal="Turn research into a punchy blog post",
    backstory="You are a storyteller who makes complex topics accessible.",
)
editor = Agent(
    role="Editor",
    goal="Polish the draft for publication",
    backstory="You are a ruthless editor who tightens every sentence.",
)

crew = Crew(
    agents=[researcher, writer, editor],
    tasks=[
        Task("Research 2026 AI-agent trends", researcher, "bullet findings"),
        Task("Write a short blog post from the findings", writer, "a draft"),
        Task("Edit the draft", editor, "publication-ready post"),
    ],
)

if __name__ == "__main__":
    final = crew.kickoff()
    print("=" * 60)
    print(final)

# --- Real version ---------------------------------------------------------
# pip install crewai
# from crewai import Agent, Task, Crew, Process
# Build the same Agents (role/goal/backstory), Tasks, and
# Crew(agents=..., tasks=..., process=Process.sequential).kickoff()
