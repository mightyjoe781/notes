# Tmux

[:octicons-arrow-left-24:{ .icon } Back](index.md) | [Detailed Guide](../tmux/index.md)

Terminal multiplexer. Keeps sessions alive after SSH disconnect, splits the terminal into panes and windows.

**Hierarchy:** Server > Sessions > Windows > Panes

### Installation

```bash
sudo apt install tmux
brew install tmux               # macOS
```

### Configuration

Edit `~/.tmux.conf`:

```bash
set -g prefix C-a               # remap prefix from C-b to C-a
unbind C-b
bind C-a send-prefix

set -g mouse on
set -g history-limit 10000
set -g base-index 1             # windows start at 1
set -g pane-base-index 1
set -g renumber-windows on

# Splits that open in current directory
bind | split-window -h -c "#{pane_current_path}"
bind - split-window -v -c "#{pane_current_path}"

# Vim-like pane navigation
bind h select-pane -L
bind j select-pane -D
bind k select-pane -U
bind l select-pane -R

# Vi keys in copy mode
set -g mode-keys vi

set -g status-style bg=colour235,fg=colour136
```

Reload config without restarting:

```bash
tmux source ~/.tmux.conf
# or inside tmux: Prefix :source ~/.tmux.conf
```

### Sessions

| Command / Binding | Action |
|---|---|
| `tmux new -s name` | create named session |
| `tmux ls` | list sessions |
| `tmux attach -t name` | attach to session |
| `tmux kill-session -t name` | kill session |
| `Prefix d` | detach from session |
| `Prefix $` | rename current session |
| `Prefix s` | interactive session picker |
| `Prefix (` / `Prefix )` | previous / next session |

### Windows

| Binding | Action |
|---|---|
| `Prefix c` | new window |
| `Prefix ,` | rename current window |
| `Prefix &` | close window (with confirm) |
| `Prefix n` / `Prefix p` | next / previous window |
| `Prefix 0-9` | jump to window by number |
| `Prefix w` | interactive window picker |
| `Prefix .` | move window to index |

### Panes

| Binding | Action |
|---|---|
| `Prefix %` | split vertically (default) |
| `Prefix "` | split horizontally (default) |
| `Prefix \|` | split vertically (if configured) |
| `Prefix -` | split horizontally (if configured) |
| `Prefix arrow` | navigate panes |
| `Prefix z` | toggle pane zoom (fullscreen) |
| `Prefix x` | close pane |
| `Prefix q` | show pane numbers |
| `Prefix {` / `Prefix }` | swap pane position |
| `Prefix Space` | cycle pane layouts |
| `Prefix !` | move pane to new window |

### Copy Mode

| Binding | Action |
|---|---|
| `Prefix [` | enter copy mode |
| `q` | exit copy mode |
| `/` | search forward |
| `?` | search backward |
| `v` | begin selection (vi mode) |
| `y` | copy selection |
| `Prefix ]` | paste |

### Tips

- Persist sessions across reboots with `tmux-resurrect` plugin
- `ssh server -t tmux attach` resumes remote session in one command
- `Prefix :setw synchronize-panes on` broadcasts keystrokes to all panes - useful for multi-server tasks
- Rename windows to reflect what is running: `Prefix ,`
- Use named sessions per project: `tmux new -s backend`, `tmux new -s frontend`

### See Also

- [tmuxcheatsheet.com](https://tmuxcheatsheet.com)
- [Config example](https://raw.githubusercontent.com/mightyjoe781/.dotfiles/refs/heads/master/tmux/.tmux.conf)
- Also: zellij (modern Rust alternative), screen (older alternative)
