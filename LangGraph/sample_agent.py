"""
LangGraph — Sample Agent: a stateful graph with conditional routing
===================================================================
Signature feature: agents modeled as a GRAPH of nodes over a shared STATE,
with conditional edges and a checkpointer that lets you pause/resume a thread.

CONCEPTUAL & self-contained — a tiny in-file engine mimics LangGraph's
StateGraph API. No API key, no `pip install langgraph` needed.

Run:  python sample_agent.py
"""
from __future__ import annotations
from typing import Callable, TypedDict

END = "__end__"


# --- The shared state passed between nodes --------------------------------
class State(TypedDict, total=False):
    question: str
    classification: str
    answer: str
    steps: list[str]


# --- A minimal StateGraph engine (this is what LangGraph gives you) -------
class StateGraph:
    def __init__(self):
        self.nodes: dict[str, Callable[[State], State]] = {}
        self.edges: dict[str, str] = {}
        self.cond: dict[str, Callable[[State], str]] = {}
        self.entry: str | None = None

    def add_node(self, name, fn): self.nodes[name] = fn
    def set_entry_point(self, name): self.entry = name
    def add_edge(self, a, b): self.edges[a] = b
    def add_conditional_edges(self, a, router): self.cond[a] = router

    def compile(self, checkpointer=None):
        return CompiledGraph(self, checkpointer)


class CompiledGraph:
    def __init__(self, g: StateGraph, checkpointer):
        self.g, self.store = g, (checkpointer if checkpointer is not None else {})

    def invoke(self, patch: State, thread_id: str = "default") -> State:
        state: State = {**self.store.get(thread_id, {}), **patch}
        state.setdefault("steps", [])
        node = self.g.entry
        while node and node != END:
            state = {**state, **self.g.nodes[node](state)}
            if node in self.g.cond:
                node = self.g.cond[node](state)
            else:
                node = self.g.edges.get(node, END)
        self.store[thread_id] = state           # persistence: resume later
        return state


# --- Mock LLM -------------------------------------------------------------
def mock_llm(prompt: str) -> str:
    p = prompt.lower()
    if "classify" in p:
        return "math" if any(c.isdigit() for c in prompt) else "general"
    if "2+2" in p or "2 + 2" in p:
        return "4"
    return "LangGraph routes work through a typed state graph."


# --- Nodes (units of work) ------------------------------------------------
def classify(state: State) -> State:
    label = mock_llm(f"classify: {state['question']}")
    return {"classification": label, "steps": state["steps"] + [f"classified={label}"]}

def answer_math(state: State) -> State:
    return {"answer": mock_llm(state["question"]), "steps": state["steps"] + ["math_node"]}

def answer_general(state: State) -> State:
    return {"answer": mock_llm(state["question"]), "steps": state["steps"] + ["general_node"]}


# --- Conditional router ---------------------------------------------------
def route(state: State) -> str:
    return "math" if state["classification"] == "math" else "general"


def build():
    g = StateGraph()
    g.add_node("classify", classify)
    g.add_node("math", answer_math)
    g.add_node("general", answer_general)
    g.set_entry_point("classify")
    g.add_conditional_edges("classify", route)
    g.add_edge("math", END)
    g.add_edge("general", END)
    return g.compile(checkpointer={})  # in-memory checkpointer == durable thread


if __name__ == "__main__":
    app = build()
    for q in ["What is 2+2?", "What is LangGraph?"]:
        out = app.invoke({"question": q}, thread_id="demo")
        print(f"Q: {q}\n  route+steps: {out['steps']}\n  answer: {out['answer']}\n")

# --- Real version ---------------------------------------------------------
# pip install langgraph langchain
# from langgraph.graph import StateGraph, END
# from langgraph.checkpoint.memory import MemorySaver
# Build the same graph; nodes call a real LLM; compile(checkpointer=MemorySaver())
# and pass config={"configurable": {"thread_id": "demo"}} to pause/resume.
