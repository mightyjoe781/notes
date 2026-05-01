# VSCode Copilot

[Reference](https://code.visualstudio.com/docs/copilot/overview)

## Components

For examples and recipes, visit: [Awesome-Copilot](https://github.com/github/awesome-copilot)

### Custom Instructions

Define common guidelines and rules that automatically influence how the AI generates code and handles development tasks.

#### Always-On Instructions

- `.github/copilot-instructions.md` — workspace-level instructions (note the plural filename)
- One or more `AGENTS.md` files
- Organization-level instructions (GitHub Enterprise)

Use `/new` or the Copilot Chat setup flow to scaffold a starter instructions file.

#### File-based Instructions

Applied when files that agent is working on match a specified pattern or if description matches the current task.

- One or more `.instructions.md` files

Example Python Instructions : [Link](https://raw.githubusercontent.com/github/awesome-copilot/refs/heads/main/instructions/python.instructions.md)

### Prompt Files

Also known as slash commands — simplify prompting for common tasks by encoding them as standalone Markdown files.

Unlike custom instructions, prompts are not applied until explicitly invoked.

Location: `.github/prompts/` folder

Examples:

- review a PR
- run tests

### Custom Agents

Configure the AI to adopt different personas tailored to specific development roles and tasks.

For example, you might create agents for a security reviewer, planner, solution architect, or other specialized roles. Each agent can have its own behavior, available tools, and instructions.

You can also use **handoffs** to create guided workflows between agents — transition seamlessly from one specialized agent to another with a single click.

Example: [Agent Conductor Workflow](https://github.com/ShepAlderson/copilot-orchestra) — a conductor/orchestra pattern where a top-level agent delegates subtasks to specialized subagents, enabling looped iterative development.

Location: `.github/agents/*.md`

### Agent Skills

Folders of instructions, scripts, and resources that load on demand to perform specialized tasks.

Skills help tailor agents for domain-specific tasks, reduce repetition, and let you compose complex workflows. They are an open standard and are loaded only when relevant.

Unlike prompts, a skill represents the *deterministic* part of a task — it encodes exactly how something should be done:

- how to run tests
- how to fetch tables from Databricks

Combine skills with `.github/scripts/` helper scripts to fully automate repetitive workflows.

### MCP

Model Context Protocol (MCP) is an open standard that lets AI models use external tools and services through a unified interface. In VS Code, MCP servers provide tools for tasks like file operations, database queries, or interacting with external APIs.

Configure MCP servers in VS Code settings or `.vscode/mcp.json` for project-scoped servers.

### Hooks

Hooks execute custom shell commands at key lifecycle points during agent sessions. Use them to automate workflows, enforce policies, validate operations, and integrate with external tools.

Use cases:

- enforce security policies
- automate code quality (run formatters like `black`, `prettier`, `gofmt`)
- create audit trails
- inject additional context before a request

Multiple hooks can be registered per lifecycle event.

## Multi-Agent Development

### Orchestra Pattern

The Conductor/Orchestra pattern is a practical multi-agent architecture: a top-level "conductor" agent breaks work into subtasks and delegates them to specialized "musician" agents, collecting and integrating their outputs.

![](assets/Pasted%20image%2020260223083118.png)

[copilot-orchestra](https://github.com/ShepAlderson/copilot-orchestra) — reference implementation for VS Code Copilot.

### Swarm Pattern

Swarms use many peer agents working in parallel on independent subtasks, with a coordinator merging results. Better suited for embarrassingly parallel tasks (e.g. scanning a large codebase for issues).

### Hierarchical Agent Systems

Multiple levels of agents where higher-level agents plan and delegate, lower-level agents execute. Useful for complex, multi-phase projects.

### Agent-to-Agent Protocols

Copilot supports handoffs — structured transitions between agents with shared context passing. This enables pipeline-style workflows where each agent's output becomes the next one's input.

