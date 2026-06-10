"""
Basics — Sample Agent: the raw ReAct loop (Reason -> Act -> Observe)
====================================================================
A CONCEPTUAL, self-contained agent. No API key, no installs — it uses a tiny
built-in mock "LLM" so you can see the agent loop that every framework in this
repo wraps and hides.

Run:  python sample_agent.py
"""

# --- Tools: the agent's "hands" -------------------------------------------
def search(query: str) -> str:
    facts = {
        "population of france": "67,000,000",
        "speed of light": "299,792,458 m/s",
    }
    return facts.get(query.lower().strip(), "no result")


def calculator(expr: str) -> str:
    # Restricted eval — only arithmetic on the characters we allow.
    if not set(expr) <= set("0123456789+-*/(). "):
        return "invalid expression"
    return str(eval(expr))  # noqa: S307 - sandboxed by the char whitelist above


TOOLS = {"search": search, "calculator": calculator}


# --- The "brain": a deterministic stand-in for an LLM ---------------------
class MockReActLLM:
    """Looks at the scratchpad and decides the next ReAct step.

    A real LLM would generate this text token-by-token. Here it is rule-based
    so the loop is reproducible and runs offline.
    """

    def next_step(self, question: str, scratchpad: list[str]) -> str:
        seen = " ".join(scratchpad).lower()
        if "67,000,000" not in seen:
            return ("Thought: I need France's population first.\n"
                    "Action: search[population of France]")
        if "33500000" not in seen and "33500000.0" not in seen:
            return ("Thought: Now I halve it.\n"
                    "Action: calculator[67000000 / 2]")
        return ("Thought: I have the answer.\n"
                "Final Answer: France's population is ~67,000,000; half is 33,500,000.")


# --- The agent loop -------------------------------------------------------
def parse_action(text: str):
    line = [l for l in text.splitlines() if l.startswith("Action:")]
    if not line:
        return None, None
    body = line[0][len("Action:"):].strip()
    tool, arg = body.split("[", 1)
    return tool.strip(), arg.rstrip("]").strip()


def run_agent(question: str, max_steps: int = 5):
    llm = MockReActLLM()
    scratchpad: list[str] = []
    print(f"QUESTION: {question}\n")
    for step in range(1, max_steps + 1):
        thought = llm.next_step(question, scratchpad)
        print(f"[step {step}]\n{thought}")
        if "Final Answer:" in thought:
            print("\nDONE.")
            return
        tool, arg = parse_action(thought)
        if tool not in TOOLS:
            print(f"Observation: unknown tool {tool!r}\n")
            continue
        observation = TOOLS[tool](arg)
        print(f"Observation: {observation}\n")
        scratchpad.append(f"{tool}({arg}) -> {observation}")
    print("Stopped: hit max steps.")


if __name__ == "__main__":
    run_agent("What is the population of France divided by 2?")

# --- Real version ---------------------------------------------------------
# Every framework here automates this loop. The simplest real version is just
# a while-loop around an LLM call (e.g. anthropic / openai) where you feed the
# model tool results back as the next user message until it stops calling tools.
