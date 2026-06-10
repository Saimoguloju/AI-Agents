/**
 * Mastra — Sample Agent: agent + tools + memory (TypeScript stack)
 * ================================================================
 * Signature feature: a full TS agent framework on top of the AI SDK — an Agent
 * bundles instructions, a model, TOOLS, and persistent MEMORY across calls.
 *
 * CONCEPTUAL & self-contained — a tiny mock mimics Mastra's Agent + createTool +
 * memory. No API key, no `npm install @mastra/core`. Pure TypeScript.
 *
 * Run:  npx tsx sample_agent.ts        (or compile with tsc)
 */

// --- createTool(): Mastra-style tool definition ---------------------------
type Tool = { id: string; description: string; execute: (input: any) => any };

function createTool(t: Tool): Tool {
  return t;
}

const addTodoTool = createTool({
  id: "add-todo",
  description: "Add an item to the todo list",
  execute: ({ item, store }: { item: string; store: string[] }) => {
    store.push(item);
    return `added '${item}'`;
  },
});

// --- A simple in-process memory (Mastra persists this for real) -----------
class Memory {
  private store: Record<string, string[]> = {};
  thread(id: string): string[] {
    return (this.store[id] ??= []);
  }
}

// --- Mock model: decides to call the tool, then summarizes ----------------
function mockModel(prompt: string, todos: string[]): { tool?: string; item?: string; text?: string } {
  const m = prompt.match(/add (.+) to my todos/i);
  if (m) return { tool: "add-todo", item: m[1] };
  if (/what.*todos/i.test(prompt)) return { text: `You have: ${todos.join(", ") || "(none)"}` };
  return { text: "I can manage your todo list." };
}

// --- Agent: instructions + model + tools + memory -------------------------
class Agent {
  constructor(
    private cfg: { name: string; instructions: string; tools: Record<string, Tool>; memory: Memory }
  ) {}

  async generate(prompt: string, threadId = "default"): Promise<string> {
    const todos = this.cfg.memory.thread(threadId);
    const decision = mockModel(prompt, todos);
    if (decision.tool) {
      const out = this.cfg.tools[decision.tool].execute({ item: decision.item, store: todos });
      console.log(`  [${this.cfg.name}] tool ${decision.tool} -> ${out}`);
      return `Done. ${out}.`;
    }
    return decision.text!;
  }
}

const agent = new Agent({
  name: "TodoAgent",
  instructions: "Help the user manage a todo list.",
  tools: { "add-todo": addTodoTool },
  memory: new Memory(),
});

async function main() {
  for (const prompt of ["Add buy milk to my todos", "Add call dentist to my todos", "What are my todos?"]) {
    console.log(`USER: ${prompt}`);
    console.log(`AGENT: ${await agent.generate(prompt, "user-1")}\n`);
  }
}

main();

/* --- Real version ---------------------------------------------------------
 * npm install @mastra/core @ai-sdk/openai      (needs OPENAI_API_KEY)
 * import { Agent } from "@mastra/core/agent";
 * import { createTool } from "@mastra/core/tools";
 * import { Memory } from "@mastra/memory";
 * import { openai } from "@ai-sdk/openai";
 * const agent = new Agent({ name: "TodoAgent", instructions: "...",
 *   model: openai("gpt-4o"), tools: { addTodo }, memory: new Memory() });
 * await agent.generate("Add buy milk to my todos", { threadId: "user-1", resourceId: "u1" });
 */
