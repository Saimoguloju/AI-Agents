"""
Semantic Kernel — Sample Agent: kernel + plugins + planner
==========================================================
Signature feature: a KERNEL hosts PLUGINS (reusable skills = native functions).
A PLANNER decomposes a goal and calls the right plugins automatically.

CONCEPTUAL & self-contained — a tiny engine mimics SK's Kernel, @kernel_function
plugins, and a planner. No API key, no `pip install semantic-kernel`.

Run:  python sample_agent.py
"""
from __future__ import annotations
import inspect


# --- Decorator marking a method as a callable skill -----------------------
def kernel_function(description: str):
    def deco(fn):
        fn.__kernel_description__ = description
        return fn
    return deco


# --- A plugin = a class of related skills ---------------------------------
class MathPlugin:
    @kernel_function("Add two numbers")
    def add(self, a: float, b: float) -> float:
        return a + b

    @kernel_function("Multiply two numbers")
    def multiply(self, a: float, b: float) -> float:
        return a * b


class TextPlugin:
    @kernel_function("Uppercase a string")
    def upper(self, text: str) -> str:
        return text.upper()


# --- The Kernel: registry of plugin functions -----------------------------
class Kernel:
    def __init__(self):
        self.functions = {}

    def add_plugin(self, plugin, name: str):
        for fname, fn in inspect.getmembers(plugin, predicate=inspect.ismethod):
            if hasattr(fn, "__kernel_description__"):
                self.functions[f"{name}.{fname}"] = fn
        return self

    def list_functions(self):
        return {k: v.__kernel_description__ for k, v in self.functions.items()}


# --- Planner: a mock LLM that turns a goal into a plugin call sequence -----
class Planner:
    def create_plan(self, kernel: Kernel, goal: str):
        # A real planner asks an LLM to choose from kernel.list_functions().
        # Here we hard-route a known goal to a deterministic plan.
        if "multiply" in goal.lower() and "uppercase" in goal.lower():
            return [
                ("MathPlugin.multiply", {"a": 6, "b": 7}),
                ("TextPlugin.upper", {"text": "the answer is {prev}"}),
            ]
        return []

    def invoke(self, kernel: Kernel, plan):
        prev = None
        for func_name, args in plan:
            args = {k: (str(prev) if v == "{prev}" else
                        v.replace("{prev}", str(prev)) if isinstance(v, str) else v)
                    for k, v in args.items()}
            result = kernel.functions[func_name](**args)
            print(f"  call {func_name}({args}) -> {result}")
            prev = result
        return prev


if __name__ == "__main__":
    kernel = Kernel().add_plugin(MathPlugin(), "MathPlugin").add_plugin(TextPlugin(), "TextPlugin")
    print("Registered skills:")
    for name, desc in kernel.list_functions().items():
        print(f"  - {name}: {desc}")

    goal = "Multiply 6 and 7, then uppercase the sentence reporting the answer."
    print(f"\nGOAL: {goal}")
    plan = Planner().create_plan(kernel, goal)
    print("FINAL:", Planner().invoke(kernel, plan))

# --- Real version ---------------------------------------------------------
# pip install semantic-kernel
# import semantic_kernel as sk
# kernel = sk.Kernel(); kernel.add_service(OpenAIChatCompletion(...))
# kernel.add_plugin(MathPlugin(), "math")
# Use FunctionCallingStepwisePlanner / auto function calling to execute a goal.
