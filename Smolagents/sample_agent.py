"""
smolagents — Sample Agent: a CodeAgent that acts by WRITING CODE
================================================================
Signature feature: instead of emitting JSON tool calls, the agent WRITES PYTHON
that calls the tools and computes the answer, then executes it.

CONCEPTUAL & self-contained — a tiny CodeAgent runs mock-generated code in a
restricted namespace of allowed tools. No API key, no `pip install smolagents`.

Run:  python sample_agent.py
"""
from __future__ import annotations


# --- Tools exposed to the agent's code --------------------------------------
def web_search(query: str) -> str:
    data = {"bridge length": 1991, "train speed": 80}  # meters, km/h
    for key, val in data.items():
        if key in query.lower():
            return str(val)
    return "0"


def final_answer(value) -> str:
    return f"FINAL ANSWER: {value}"


ALLOWED_TOOLS = {"web_search": web_search, "final_answer": final_answer}


# --- Mock "code LLM": produces a Python snippet that uses the tools --------
class MockCodeModel:
    def write_code(self, task: str) -> str:
        # A real model generates this from the task. It reasons in code:
        return (
            "length_m = int(web_search('bridge length'))\n"
            "speed_kmh = int(web_search('train speed'))\n"
            "speed_ms = speed_kmh * 1000 / 3600\n"
            "seconds = round(length_m / speed_ms, 1)\n"
            "final_answer(f'{seconds} seconds to cross')\n"
        )


# --- CodeAgent: generate code -> execute it in a tool-only sandbox --------
class CodeAgent:
    def __init__(self, tools: dict, model: MockCodeModel):
        self.tools, self.model = tools, model

    def run(self, task: str) -> str:
        code = self.model.write_code(task)
        print("Agent wrote and is executing this code:\n" + "-" * 40)
        print(code + "-" * 40)
        captured = {}
        # Sandbox: only the allowed tools are in scope (no builtins import etc.)
        sandbox = {"__builtins__": {"int": int, "round": round}, **self.tools}

        def capturing_final_answer(value):
            captured["result"] = self.tools["final_answer"](value)
            return captured["result"]

        sandbox["final_answer"] = capturing_final_answer
        exec(code, sandbox)            # noqa: S102 - scope limited to allowed tools
        return captured.get("result", "no final_answer called")


if __name__ == "__main__":
    agent = CodeAgent(ALLOWED_TOOLS, MockCodeModel())
    task = "How long does an 80 km/h train take to cross a 1991 m bridge?"
    print(f"TASK: {task}\n")
    print("\n" + agent.run(task))

# --- Real version ---------------------------------------------------------
# pip install smolagents
# from smolagents import CodeAgent, WebSearchTool, InferenceClientModel
# agent = CodeAgent(tools=[WebSearchTool()], model=InferenceClientModel())
# agent.run("How long does an 80 km/h train take to cross a 1991 m bridge?")
