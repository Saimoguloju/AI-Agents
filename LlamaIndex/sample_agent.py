"""
LlamaIndex — Sample Agent: agentic RAG (decide WHEN to retrieve)
================================================================
Signature feature: documents are indexed and exposed as a query-engine TOOL.
An agent decides whether a question needs retrieval, queries the index, and
grounds its answer in the retrieved chunks.

CONCEPTUAL & self-contained — a tiny TF-style index + agent mimic LlamaIndex's
VectorStoreIndex + QueryEngineTool + AgentWorkflow. No API key, no install.

Run:  python sample_agent.py
"""
from __future__ import annotations
from dataclasses import dataclass


# --- "Documents" ----------------------------------------------------------
DOCS = [
    "The Eiffel Tower is 330 meters tall and located in Paris, France.",
    "LlamaIndex is a data framework for building agentic RAG applications.",
    "RAG combines retrieval with generation to ground answers in real data.",
]


# --- A naive index: keyword overlap stands in for vector similarity -------
class VectorStoreIndex:
    def __init__(self, docs: list[str]):
        self.docs = docs

    def retrieve(self, query: str, k: int = 1) -> list[str]:
        q = set(query.lower().split())
        scored = sorted(self.docs, key=lambda d: len(q & set(d.lower().split())), reverse=True)
        top = [d for d in scored if q & set(d.lower().split())][:k]
        return top


# --- The index turned into a TOOL the agent can call ----------------------
@dataclass
class QueryEngineTool:
    index: VectorStoreIndex
    name: str = "knowledge_base"
    description: str = "Search the indexed documents for grounding facts."

    def __call__(self, query: str) -> str:
        hits = self.index.retrieve(query)
        return hits[0] if hits else "no relevant document found"


# --- Agent that decides WHEN to retrieve (agentic RAG) --------------------
class RagAgent:
    def __init__(self, tool: QueryEngineTool):
        self.tool = tool

    def _needs_retrieval(self, q: str) -> bool:
        # A real agent lets the LLM decide; here: greetings need no retrieval.
        return not any(g in q.lower() for g in ("hi", "hello", "thanks"))

    def chat(self, question: str) -> str:
        if not self._needs_retrieval(question):
            print(f"  [agent] no retrieval needed for: {question!r}")
            return "Hello! Ask me about the Eiffel Tower or RAG."
        print(f"  [agent] retrieving for: {question!r}")
        context = self.tool(question)
        print(f"  [agent] retrieved: {context}")
        return f"Based on the docs: {context}"


if __name__ == "__main__":
    index = VectorStoreIndex(DOCS)
    agent = RagAgent(QueryEngineTool(index))
    for q in ["Hello there", "How tall is the Eiffel Tower?", "What is RAG?"]:
        print(f"\nQ: {q}\nA: {agent.chat(q)}")

# --- Real version ---------------------------------------------------------
# pip install llama-index            (needs OPENAI_API_KEY by default)
# from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
# from llama_index.core.tools import QueryEngineTool
# from llama_index.core.agent.workflow import FunctionAgent
# index = VectorStoreIndex.from_documents(SimpleDirectoryReader("data").load_data())
# agent = FunctionAgent(tools=[QueryEngineTool.from_defaults(index.as_query_engine())], llm=...)
