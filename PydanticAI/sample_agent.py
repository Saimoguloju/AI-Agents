"""
Pydantic AI — Sample Agent: type-safe, validated structured output
==================================================================
Signature feature: you declare the EXACT output shape; the agent returns a
VALIDATED object (not a string), and retries/self-corrects if validation fails.

CONCEPTUAL & self-contained — uses a stdlib dataclass + a hand-rolled validator
to mimic Pydantic AI's output_type contract. No API key, no `pip install pydantic-ai`.

Run:  python sample_agent.py
"""
from __future__ import annotations
from dataclasses import dataclass


# --- The EXACT output you want (a Pydantic model in the real thing) -------
@dataclass
class CityInfo:
    city: str
    country: str
    population: int

    def __post_init__(self):
        if not isinstance(self.population, int) or self.population <= 0:
            raise ValueError("population must be a positive int")
        if not self.country:
            raise ValueError("country is required")


# --- Mock LLM that sometimes returns bad data so we can show self-correction
class MockLLM:
    def __init__(self):
        self.attempt = 0

    def structured(self, prompt: str) -> dict:
        self.attempt += 1
        if self.attempt == 1:
            # First try: invalid (population as string) -> triggers a retry
            return {"city": "Paris", "country": "France", "population": "many"}
        return {"city": "Paris", "country": "France", "population": 2_100_000}


# --- A typed agent: enforces output_type, retries on validation failure ---
class Agent:
    def __init__(self, output_type, retries: int = 2):
        self.output_type, self.retries, self.llm = output_type, retries, MockLLM()
        self.tools = {}

    def tool(self, fn):                 # @agent.tool decorator
        self.tools[fn.__name__] = fn
        return fn

    def run_sync(self, prompt: str):
        last_err = None
        for n in range(1, self.retries + 2):
            raw = self.llm.structured(prompt)
            try:
                obj = self.output_type(**raw)
                print(f"[attempt {n}] valid -> {obj}")
                return obj
            except (ValueError, TypeError) as e:
                last_err = e
                print(f"[attempt {n}] INVALID ({e}); feeding error back to model...")
        raise RuntimeError(f"failed after retries: {last_err}")


agent = Agent(output_type=CityInfo)


@agent.tool
def lookup_population(city: str) -> int:
    return {"paris": 2_100_000}.get(city.lower(), 0)


if __name__ == "__main__":
    result = agent.run_sync("Give me structured info about Paris.")
    print("\nTyped result is a real object:")
    print(f"  result.city       = {result.city}")
    print(f"  result.population = {result.population:,}")

# --- Real version ---------------------------------------------------------
# pip install pydantic-ai
# from pydantic import BaseModel
# from pydantic_ai import Agent
# class CityInfo(BaseModel): city: str; country: str; population: int
# agent = Agent("openai:gpt-4o", output_type=CityInfo)
# result = agent.run_sync("..."); result.output  # validated CityInfo
