# VSCode Copilot

[Reference](https://code.visualstudio.com/docs/copilot/overview)

## Components

For example of all recipes visit : [Awesome-Copilot](https://github.com/github/awesome-copilot)
### Custom Instructions

Enable to define common guidelines and rules that automatically influence how AI generates code, handles the development task.

#### Always On Instructions

- `.github/copilot-instruction.md`
- One or more `AGENTS.md` files
- Organization-level instructions
- `CLAUDE.md`

Use `/init` to create a started template.
#### File-based Instructions

Applied when files that agent is working on match a specified pattern or if description matches the current task.

- One or more `.instructions.md` files

Example Python Instructions : [Link](https://raw.githubusercontent.com/github/awesome-copilot/refs/heads/main/instructions/python.instructions.md)

### Prompt Files

also known as slash commands, simplify prompting for common tasks by encoding them as standalone Markdown files.

Unlike custom instruction, prompt are not applied until invoked.

Location : `.github/prompts` folder

Example :

- review a PR
- run tests

### Custom Agents

configure the AI to adopt different personas tailored to specific development roles and tasks.

For example, you might create agents for a security reviewer, planner, solution architect, or other specialized roles. Each persona can have its own behavior, available tools, and instructions.

You can also use handoffs to create guided workflows between agents. Transition seamlessly from one specialized agent to another with a single select.

Example : [Agent Conductor Workflow](https://github.com/ShepAlderson/copilot-orchestra) : Closely resembles ralph wiggum plugin from claude using looped development.

Location : `.github/agents/*.md`
### Agent Skills

Folders of instruction, scripts and resources that load on demand to perform specialized tasks.

Help tailor agents for domain specific task, reducing repetition, and let you compose complex workflow.

Its an open standard and loaded on demand.

As compared to prompt its deterministic part of a task.

- how to run tests
- fetch tables from databricks

I usually combine skills with `.github/scripts/` and putting some helper scripts to automate the skill.

### MCP

Model Context Protocol (MCP) is an open standard that lets AI models use external tools and services through a unified interface. In VS Code, MCP servers provide tools for tasks like file operations, databases, or interacting with external APIs.

### Hooks

Hooks enable you to execute custom shell commands at key lifecycle points during agent sessions. Use hooks to automate workflows, enforce security policies, validate operations, and integrate with external tools.

Use cases :

- enforce security policies
- automate code quality : run formatters
- create audit trail
- inject context

You can hook multiple lifecycle events.
## Multi-Agent development

### Swarms

### Orchestra

A simple pattern I found easier to use is Conductor Orchestra.

High Level Working

![](assets/Pasted%20image%2020260223083118.png)

[Link](https://github.com/ShepAlderson/copilot-orchestra)

### Multi-Agent Framework

### Hierarchical Agent Systems

### Agent-to-Agent Protocols


