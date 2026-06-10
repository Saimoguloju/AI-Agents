/**
 * Vercel AI SDK — Sample Agent: unified provider + tool calling
 * =============================================================
 * Signature feature: one unified API (generateText / streamText) across
 * providers, with TOOLS the model can call in a multi-step loop.
 *
 * CONCEPTUAL & self-contained — a tiny mock mimics the AI SDK's generateText +
 * tool() shape. No API key, no `npm install ai`. Pure TypeScript.
 *
 * Run:  npx tsx sample_agent.ts        (or compile with tsc)
 */

// --- tool(): mirrors the AI SDK's tool definition shape -------------------
type Tool<A, R> = {
  description: string;
  execute: (args: A) => Promise<R> | R;
};

function tool<A, R>(t: Tool<A, R>): Tool<A, R> {
  return t;
}

const weatherTool = tool({
  description: "Get the current weather for a city",
  execute: ({ city }: { city: string }) => ({ city, tempC: 24, sky: "sunny" }),
});

// --- Mock "model": decides whether to call a tool, then answers -----------
type Step = { type: "tool-call"; tool: string; args: any } | { type: "text"; text: string };

function mockModel(prompt: string, toolResults: any[]): Step {
  if (toolResults.length === 0 && /weather/i.test(prompt)) {
    const city = prompt.match(/in (\w+)/i)?.[1] ?? "Paris";
    return { type: "tool-call", tool: "weather", args: { city } };
  }
  const w = toolResults[0];
  return { type: "text", text: w ? `It's ${w.tempC}C and ${w.sky} in ${w.city}.` : "I can answer weather questions." };
}

// --- generateText: the multi-step agent loop the SDK runs for you ---------
async function generateText(opts: {
  prompt: string;
  tools: Record<string, Tool<any, any>>;
  maxSteps?: number;
}): Promise<string> {
  const results: any[] = [];
  for (let step = 0; step < (opts.maxSteps ?? 5); step++) {
    const action = mockModel(opts.prompt, results);
    if (action.type === "text") {
      return action.text;
    }
    console.log(`  [step ${step}] tool-call ${action.tool}(${JSON.stringify(action.args)})`);
    const out = await opts.tools[action.tool].execute(action.args);
    console.log(`  [step ${step}] result ${JSON.stringify(out)}`);
    results.push(out);
  }
  return "stopped: max steps";
}

async function main() {
  const prompt = "What is the weather in Paris?";
  console.log(`USER: ${prompt}`);
  const text = await generateText({ prompt, tools: { weather: weatherTool }, maxSteps: 5 });
  console.log(`AGENT: ${text}`);
}

main();

/* --- Real version ---------------------------------------------------------
 * npm install ai @ai-sdk/openai            (needs OPENAI_API_KEY)
 * import { generateText, tool } from "ai";
 * import { openai } from "@ai-sdk/openai";
 * import { z } from "zod";
 * const { text } = await generateText({
 *   model: openai("gpt-4o"),
 *   tools: { weather: tool({ description: "...",
 *     parameters: z.object({ city: z.string() }),
 *     execute: async ({ city }) => ({ city, tempC: 24 }) }) },
 *   maxSteps: 5,
 *   prompt: "What is the weather in Paris?",
 * });
 */
