"""
MetaGPT — Sample Agent: an AI software company (Code = SOP(Team))
=================================================================
Signature feature: one requirement flows through a fixed SOP of role agents —
ProductManager -> Architect -> ProjectManager -> Engineer -> QA — each
producing a STANDARDIZED ARTIFACT that the next role consumes.

CONCEPTUAL & self-contained — a tiny Team runs the SOP with mock roles.
No API key, no `pip install metagpt`.

Run:  python sample_agent.py
"""
from __future__ import annotations
from dataclasses import dataclass


# --- A Role produces one artifact from the previous artifact --------------
@dataclass
class Role:
    name: str

    def act(self, requirement: str, incoming: str) -> str:
        if self.name == "ProductManager":
            return f"PRD: build '{requirement}'. Users want add/list todos. Acceptance: CLI works."
        if self.name == "Architect":
            return "DESIGN: module todo.py with add_todo(), list_todos(); in-memory list store."
        if self.name == "ProjectManager":
            return "TASKS: 1) implement add_todo 2) implement list_todos 3) write tests."
        if self.name == "Engineer":
            return ("CODE:\n"
                    "TODOS = []\n"
                    "def add_todo(t): TODOS.append(t)\n"
                    "def list_todos(): return list(TODOS)")
        if self.name == "QA":
            ok = "add_todo" in incoming and "list_todos" in incoming
            return f"QA REPORT: {'PASS - both functions present.' if ok else 'FAIL'}"
        return "..."


# --- The Team runs the standard operating procedure -----------------------
class Team:
    SOP = ["ProductManager", "Architect", "ProjectManager", "Engineer", "QA"]

    def run_project(self, requirement: str) -> dict[str, str]:
        print(f"REQUIREMENT: {requirement}\n")
        artifacts: dict[str, str] = {}
        incoming = requirement
        for role_name in self.SOP:
            artifact = Role(role_name).act(requirement, incoming)
            artifacts[role_name] = artifact
            print(f">>> {role_name}\n{artifact}\n")
            incoming = artifact            # hand the artifact to the next role
        return artifacts


if __name__ == "__main__":
    Team().run_project("a command-line todo app")

# --- Real version ---------------------------------------------------------
# pip install metagpt                (needs an LLM API key configured)
# from metagpt.software_company import generate_repo
# repo = generate_repo("a command-line todo app")
# # MetaGPT runs the full SOP and writes PRD, design docs, code, and tests to disk.
