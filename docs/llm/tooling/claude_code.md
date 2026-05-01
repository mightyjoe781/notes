# Claude Code

A brief guide to Claude Code features. Refer to the [official docs](https://docs.anthropic.com/en/claude-code/) for the latest updates.

## Setup

### Installation

```bash
# CLI via npm (recommended)
npm install -g @anthropic-ai/claude-code

# macOS desktop app
brew install --cask claude-code
```

Platform-specific installation: [Official Docs](https://docs.anthropic.com/en/claude-code/quickstart)

Install the Claude Code extension in VS Code. Open a terminal and type `claude` for the terminal interface. The Claude Code Chat window also supports attaching files and images (similar to the desktop app).

### Configuration

There are two levels of configuration: `global` (`~/.claude/settings.json`) and `local` to the project.

Use the `claude` CLI to make config changes with the `/config` command.

Full configuration reference: [Official Docs](https://docs.anthropic.com/en/claude-code/settings)

An important setting is preventing Claude from reading secrets:

```json
{
    "env": {
        "CLAUDE_CODE_HIDE_ACCOUNT_INFO": "1"
    },
    "permissions": {
        "deny": [
            "Bash(**/.env)",
            "Read(**/.env)",
            "Write(**/.env)"
        ]
    },
    "model": "claude-sonnet-4-5"
}
```

Create a `.claude` directory local to the project with `.claude/settings.json`, and add project-specific overrides in `.claude/settings.local.json`.

### Slash Commands

- `/clear` — clears the session and context memory; useful for managing token budget
- `/status` — prints context usage, system prompt usage, MCP tool usage, autocompact buffer status, etc.
- `/usage` — shows remaining Claude Code usage quota
- `/resume` — resume a previous session
- `/compact` — compact context to free up token space
- `/rewind` — undo the last change Claude made

Claude can be invoked directly with a prompt or in headless (non-interactive) mode:

```bash
claude "explain this project"

# headless / non-interactive
claude -p "explain this project"
```

Other useful flags:

```bash
claude -c          # resume last session
```

- `Shift+Tab` — toggle auto-accept edits mode (accepts file edits without prompting, but still prompts for shell commands)
- For trusted environments: `claude --dangerously-skip-permissions`

A safer approach is to use the built-in sandbox or a Docker container:

```bash
# built-in sandbox (in a session)
/sandbox   # auto-allow mode is recommended

# Docker: run Claude in an isolated container
docker run -it --rm -v $(pwd):/workspace ghcr.io/anthropics/claude-code:latest \
  --dangerously-skip-permissions
```

Reverting changes:

```bash
# /rewind — undo last Claude change
# TIP: commit frequently so you can git reset to a known-good state
```

## Usage

### Prompts & Context

Keep prompts concise and precise. Good prompts combine: **specific instructions** + **relevant context**.

When starting from scratch, write a detailed spec document first — refine it with an LLM, get a technical breakdown, then use it to guide Claude Code. Always let Claude review and update the spec to reflect what it can actually do.

Reference files inline with `@filename` in the chat to attach them as context.

### Memory & System Instructions

Claude uses `CLAUDE.md` for persistent instructions and long-term memory — it is always loaded into the context. Multiple `CLAUDE.md` files can exist at different directory levels (project root, subdirectories), and they are all loaded when Claude operates in those directories.

Claude also has an auto-memory system stored at `~/.claude/projects/<project>/memory/MEMORY.md`. Claude selectively loads relevant memory entries at the start of each conversation and can maintain multiple memory files organized by topic or skill.

### Plan Mode

Plan Mode (`/plan`) puts Claude into a think-first workflow: it produces a structured plan and waits for approval before executing. This mirrors the Think → Plan → Act paradigm common in modern coding agents.

Use it for non-trivial tasks where you want to review the approach before any files are changed. Claude will outline steps, identify files it intends to touch, and surface trade-offs.

### Built-in Tools (MCP, Agent, Skill)

Let's say you want to include context about best practices from docs website, there are two ways.

- Include context by using files or pasting links to docs
- Add MCP servers related to docs, and it can search whenever needed. Example - `context7`

Use `/mcp` to manage MCP servers. MCP servers can be installed locally (project-scoped) or globally.

An even better approach is to create a dedicated Agent for a recurring task (e.g. searching docs), so you don't have to re-specify context each time.

**Agent Skills** are extra, dynamically loaded context bundles. Example: React Component Best Practices. Skills are only loaded when relevant, keeping baseline context lean.

```
SKILL.md
[+ extra .md documents]
[+ references/ folder]
[+ scripts/ folder]
[+ assets/ folder]
```

Find community skills at the [`anthropics/claude-code`](https://github.com/anthropics/claude-code) repo and at [skills.sh](https://skills.sh/). Use the built-in `skill-creator` skill to scaffold new ones.

> Claude Code has image vision — you can paste screenshots directly into the chat.

### Hooks

Hooks execute custom shell commands at key lifecycle points during a Claude Code session. Targets can be shell commands, HTTP endpoints, or LLM sub-prompts.

Examples: run `gofmt` or `tflint` automatically after every file edit.

More on Hooks: [Official Docs](https://docs.anthropic.com/en/claude-code/hooks)

### Automated Iterative Loops

The `/loop` command (or the `loop` skill in Claude Code) lets you run a prompt repeatedly on a schedule or in a continuous cycle. Useful for things like "keep running tests until they pass" or polling a build.

External inspiration: [Ralph](https://github.com/snarktank/ralph) — an early looped LLM development pattern that influenced how modern coding agents handle iterative task execution.

