# Claude Code

Following is a very brief guide on feature in claude code ! Refer to full documentation for latest updates!

## Setup

### Installation

```
brew install --cask claude-code
```

Platform Specific Installation : [Official Docs](https://code.claude.com/docs/en/quickstart#native-install-recommended)

Install Claude Code Plugin in VS-Code. Open terminal and type `claude` for terminal interface. There is another interaction using Claude Code Chat window where you can attach files and images as well (Similar to Desktop App)

### Configuration

There are two levels of configuration : `global` (`~/.claude/settings.json` dir) and `local` to the project.

Use `claude` CLI itself to make config changes using `/config` command.

Full Configuration : https://code.claude.com/docs/en/settings

A very important setting is not allowing claude to read secrets.

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
    "model": "opus",
    "alwaysThinkingEnabled": "false"
}

```

Create a `.claude` local to project and create `.claude/settings.json` in the project and add additional override using `.claude/settings.local.json`

### Slash Command

- `/clear` : clears the session and clears the context memory. Very useful to manage tokens.
- `/context` : Prints context usage, System Prompts usage, MCP tools Usage etc, autocompact buffer usage etc,
- `/usage` : shows remaining usage for the claude code

Claude can be invoked directly using a prompt or in a headless mode

```bash
claude "explain this project"

# headless
claude -p "explain this project"
```

- `/resume` : resume old sessions
- `claude -c` : for last session,
- `shift+tab` : accept edits mode, its only allowed to create edits, not the command. (default it will ask all edits)
- For risk takers :) - start claude with following command : `claude --dangerously-skip-permissions`

A safer approach is to use docker-sandbox to run above command or native sandbox

```bash
# docker sandbox
docker sandbox run claude # default is dangerous-skip-permissions

# built-in sandbox, in a session
/sandbox : auto-allow mode is preferred!
```

Reverting the changes to a previous state,

```bash
# using git
# TIP: create commits frequently !

# Esc-Esc (twice) to revert last change
# or /rewind command
```

## Usage

### Prompts & Context

Generally its a good idea to have your prompts as clear/crisp as possible, Concise & Precise. Good Prompts are just a combination of : Specific Instructions + Relevant Information/Extra Information.

When working from scratch its alway a better idea to have detailed spec document, which could be refined using LLM itself, get the technical document in detail from LLM and use it guide Claude Code.

Always let Claude Code revise the spec, to improve and conform document to its capability. To specify use `@filename` in chats.

### Memory & System Instruction

Claude uses `claude.MD` for the persistent instructions/long-term memory to define session information which is always loaded. There could be many `claude.MD` files.

Claude also has Auto-Memory for this as well. This is stored at `~/.claude/projects/project/memory/MEMORY.md`. Usually claude loads parts of the memory for every new conversation and there could many Memory files even for multiple skills or conversation claude finds useful to store.

### Plan Mode

Now most of the agents already follow the paradigm of Think, Plan, Prompt out of box like Github Copilot.

Usually it sets the path for operation of the claude code. A better example of the repo is copilot-orchestra.

### Built-in Tools (MCP, Agent, Skill)

Let's say you want to include context about best practices from docs website, there are two ways.

- Include context by using files or pasting links to docs
- Add MCP servers related to docs, and it can search whenever needed. Example - `context7`

Use `/mcp` to manage MCP servers, and MCP servers can be installed locally/globally.

Even better approach is create an Agent for this task of searching Docs, helping you to avoid specifying these things again and again

Create Agent Skills are extra, dynamically loaded, context. Example : React Component Best Practices.

```
SKILL.md
[+ extra .md documents]
[+ references/ folder]
[+ scripts/ folder]
[+ assets/ folder]
```

Use `anthropics/skills` repo to find useful skills, and use `skill-creator to create skills`. For skills only metadata is loaded and they are loaded only when required.

Another famous repo is https://skills.sh/

NOTE: claude-code has image vision, so you can paste images as well.

### Hooks

Hooks enable you to execute custom shell commands at key lifecycle points during agent sessions. You can use HTTP endpoints, or LLM prompts as well.

Example : `gofmt` or `tflint` etc for formatting the code.

More on Hooks here : https://code.claude.com/docs/en/hooks

### Automated Iterative Loops

Read more on Ralph Loop here -  https://github.com/snarktank/ralph

