# AI Agents

An agent is an LLM that can take actions - calling tools, running code, browsing the web - and loop until it completes a goal. The model decides what to do next based on its current context and tool results.

## What Makes an Agent

A basic agent needs:
- **LLM** - the reasoning engine
- **Tools** - functions the model can invoke (search, calculator, code runner, APIs)
- **Loop** - observe result, decide next action, repeat until done
- **Memory** - track state across steps

```
User goal
  -> LLM decides action
  -> Execute tool
  -> Add result to context
  -> LLM decides next action
  -> ... repeat ...
  -> LLM produces final answer
```

## Tool Use / Function Calling

Most LLM APIs support structured tool definitions. The model outputs a tool name + arguments (as JSON), your code executes it, and the result goes back as context.

```python
import anthropic

client = anthropic.Anthropic()
tools = [
    {
        "name": "get_weather",
        "description": "Get current weather for a city",
        "input_schema": {
            "type": "object",
            "properties": {
                "city": {"type": "string", "description": "City name"}
            },
            "required": ["city"]
        }
    }
]

response = client.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=1024,
    tools=tools,
    messages=[{"role": "user", "content": "What's the weather in Tokyo?"}]
)

# Check if model wants to use a tool
if response.stop_reason == "tool_use":
    tool_use = next(b for b in response.content if b.type == "tool_use")
    tool_name = tool_use.name        # "get_weather"
    tool_input = tool_use.input      # {"city": "Tokyo"}
    # ... execute tool, send result back ...
```

## Memory Types

| Type | Storage | Scope | Example |
|---|---|---|---|
| In-context | Prompt window | Single session | Conversation history |
| External/vector | Vector DB | Cross-session | User preferences, past docs |
| Episodic | Files/DB | Persistent | Summary of past sessions |
| Semantic | Model weights | Permanent | Pre-trained knowledge |

In practice: use in-context memory for the current task, summarize + store important facts to external storage between sessions.

## Planning Patterns

### ReAct (Reason + Act)

Interleave reasoning (Thought) and action (Act) steps. The model explains its reasoning before each tool call.

```
Thought: I need to find the current price of AAPL stock.
Action: search("AAPL stock price today")
Observation: AAPL is trading at $213.45 as of market close.
Thought: I have the price. I can now answer.
Answer: AAPL closed at $213.45 today.
```

Simple and effective. Most modern agents use a variant of this internally.

### Plan-then-Execute

First produce a full plan, then execute each step. Better for complex multi-step tasks where you don't want to lose track of the overall goal.

```
Plan:
  1. Search for the company's latest earnings report
  2. Extract revenue, profit, and guidance figures
  3. Compare to analyst estimates
  4. Write a 200-word summary

Executing step 1...
```

### Reflexion

After completing a task, the agent reflects on what went wrong and produces a refined attempt. Useful when the environment gives clear pass/fail signals (e.g. code that runs or doesn't).

## Multi-Agent Patterns

Single agents hit limits on complex tasks - context fills up, reasoning degrades on very long chains. Multi-agent systems split the work.

### Orchestrator + Subagents

A top-level agent breaks work into subtasks and delegates to specialized agents. Each subagent has its own context, tools, and focus.

```python
# Conceptual structure with Claude Code SDK
orchestrator = Agent(
    model="claude-opus-4-7",
    instructions="You coordinate research tasks. Delegate to subagents."
)
researcher = Agent(model="claude-sonnet-4-5", tools=[web_search])
writer = Agent(model="claude-sonnet-4-5", tools=[file_write])
```

### Swarm

Many peer agents work in parallel on independent subtasks; results are merged. Better for embarrassingly parallel work (scanning a large codebase, processing many documents).

### Critic / Verifier

A separate agent reviews the output of the main agent and provides feedback for refinement. Cheaper than human review, effective for code correctness and factual checks.

## Common Frameworks

| Framework | Best for |
|---|---|
| LangGraph | Stateful, graph-based agent workflows |
| CrewAI | Multi-agent collaboration, role-based |
| Claude Code SDK | Coding agents, agentic code tasks |
| AutoGen (Microsoft) | Conversational multi-agent |
| Pydantic AI | Type-safe agents in Python |

## Key Failure Modes

- **Infinite loops** - always set a max_iterations limit
- **Context overflow** - long tool outputs fill the window; summarize or truncate
- **Cascading errors** - one bad tool result poisons downstream steps; add verification steps
- **Tool misuse** - model calls tool with wrong arguments; use strict input schemas + examples
- **Over-planning** - agent plans forever instead of acting; limit plan length

## Practical Tips

- Start with a single agent + tools before going multi-agent
- Log every tool call and result - agents are hard to debug without traces
- Set conservative limits: max iterations, max tokens per tool result, timeouts
- Give agents an "I don't know" escape hatch so they don't hallucinate tool results
- Prefer deterministic tools (code execution, APIs) over non-deterministic ones (web search) when possible
