"""
Mirascope — Sample Agent: the LLM "anti-framework"
==================================================
Signature feature: a plain DECORATED FUNCTION *is* the LLM call. You stay close
to the metal, get typed/structured output, and swap providers without rewriting
your structure.

CONCEPTUAL & self-contained — a decorator mimics Mirascope's @llm.call with a
mock provider and dataclass "response_model". No API key, no `pip install mirascope`.

Run:  python sample_agent.py
"""
from __future__ import annotations
from dataclasses import dataclass, fields
import functools


# --- The structured output you want back ----------------------------------
@dataclass
class Book:
    title: str
    author: str
    year: int


# --- Mock provider registry (swap "openai" / "anthropic" freely) ----------
def _mock_provider(provider: str, model: str, prompt: str) -> dict:
    print(f"  [{provider}:{model}] prompt -> {prompt}")
    return {"title": "Dune", "author": "Frank Herbert", "year": 1965}


# --- The @llm.call decorator: the function body returns the PROMPT ---------
def call(provider: str, model: str, response_model=None):
    def deco(fn):
        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
            prompt = fn(*args, **kwargs)               # function body builds the prompt
            raw = _mock_provider(provider, model, prompt)
            if response_model is None:
                return raw
            allowed = {f.name for f in fields(response_model)}
            return response_model(**{k: v for k, v in raw.items() if k in allowed})
        return wrapper
    return deco


# --- A plain function that IS the LLM call --------------------------------
@call(provider="openai", model="gpt-4o", response_model=Book)
def recommend_book(genre: str) -> str:
    return f"Recommend one classic {genre} book."


if __name__ == "__main__":
    book = recommend_book("science fiction")
    print("\nTyped result (a real Book object):")
    print(f"  {book.title} by {book.author} ({book.year})")
    print(f"  type = {type(book).__name__}")

# --- Real version ---------------------------------------------------------
# pip install "mirascope[openai]"    (needs OPENAI_API_KEY)
# from mirascope import llm
# from pydantic import BaseModel
# class Book(BaseModel): title: str; author: str; year: int
# @llm.call(provider="openai", model="gpt-4o", response_model=Book)
# def recommend_book(genre: str) -> str: return f"Recommend one classic {genre} book."
# # Swap to provider="anthropic", model="claude-..." with no structural change.
