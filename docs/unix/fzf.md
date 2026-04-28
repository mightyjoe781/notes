# fzf

[:octicons-arrow-left-24:{ .icon } Back](index.md)

Interactive fuzzy finder for the terminal. Filters any list: files, history, processes, git branches.

### Installation

```bash
sudo apt install fzf
brew install fzf

# Shell integrations (key bindings + completion)
$(brew --prefix)/opt/fzf/install     # macOS
/usr/share/doc/fzf/examples/install  # Debian
```

### Basic Usage

```bash
fzf                                  # search files in current directory
ls | fzf                             # filter any list
history | fzf                        # search history
cat /etc/passwd | fzf                # filter passwd entries
```

### Key Bindings (after shell integration)

| Binding | Action |
|---|---|
| `Ctrl+r` | fuzzy search command history |
| `Ctrl+t` | insert selected file path into command line |
| `Alt+c` | cd into selected directory |

### Flags Reference

| Flag | Description |
|---|---|
| `--preview CMD` | show preview panel |
| `--multi` / `-m` | multi-select with Tab |
| `--query STR` | start with initial query |
| `--select-1` | auto-select if only one match |
| `--exit-0` | exit if no match |
| `--height N%` | compact mode |
| `--layout=reverse` | show list below prompt |
| `--ansi` | parse ANSI color codes |
| `--bind KEY:ACTION` | custom key binding |
| `-0` | null-delimited input |

### Common Patterns

```bash
# Open file in editor
vim $(fzf)
vim $(fzf --preview 'bat --color=always {}')

# cd into directory
cd $(find . -type d | fzf)

# Kill process
kill $(ps aux | fzf | awk '{print $2}')

# Checkout git branch
git checkout $(git branch -a | fzf | tr -d ' ')

# Preview file contents
fzf --preview 'cat {}'
fzf --preview 'bat --color=always --style=numbers {}'

# Preview with syntax highlight (requires bat)
rg --files | fzf --preview 'bat --color=always {}'

# Multi-select and delete files
find . -name "*.log" | fzf -m | xargs rm
```

### Shell Functions

```zsh
# fe - fuzzy open file in $EDITOR
fe() {
    local files
    IFS=$'\n' files=($(fzf --multi --select-1 --exit-0 --query="$1"))
    [[ -n "$files" ]] && ${EDITOR:-vim} "${files[@]}"
}

# fcd - fuzzy cd
fcd() {
    local dir
    dir=$(fd . "${1:-.}" --type=d 2>/dev/null | fzf --no-multi --height=40%) &&
    cd "$dir"
}

# fta - fuzzy tmux attach
fta() {
    local session
    session=$(tmux list-sessions -F "#{session_name}" |
        fzf --height=20% --select-1 --exit-0 --query="$1") &&
    tmux attach -t "$session"
}

# flog - fuzzy git log browser
flog() {
    git log --oneline --color=always |
    fzf --ansi --preview 'git show --color=always {1}' |
    awk '{print $1}'
}
```

### Tips

- Combine with `rg` for live grep: `rg --color=always "" | fzf --ansi`
- Set `FZF_DEFAULT_COMMAND='rg --files --hidden'` to use rg instead of find
- Set `FZF_DEFAULT_OPTS='--height 40% --layout=reverse --border'` for compact UI
- `fd` is faster than `find` for the directory listing source

### See Also

- [ripgrep](ripgrep.md) for the search backend
- Also: skim (fzf clone in Rust), peco, fzy
