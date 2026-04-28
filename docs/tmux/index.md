# tmux

tmux is a terminal multiplexer - it lets you run multiple terminal sessions inside a single window, detach from them, and reattach later. Sessions survive disconnects, making it essential for remote work.

---

## Quick Start

```bash
tmux new -s work          # start a named session
# do stuff, then detach:
PREFIX d                  # detach (session keeps running)
tmux ls                   # list running sessions
tmux a -t work            # reattach
```

Inside a session, split the screen and navigate:

```
PREFIX "   split pane top/bottom
PREFIX %   split pane left/right
PREFIX o   cycle between panes
PREFIX z   zoom a pane (toggle fullscreen)
PREFIX d   detach from session
```

---

## Quick Reference

### Sessions

| Key / Command | Action |
|---|---|
| `tmux new -s <name>` | New named session |
| `tmux ls` | List sessions |
| `tmux a -t <name>` | Attach to session |
| `tmux kill-session -t <name>` | Kill session |
| `PREFIX d` | Detach |
| `PREFIX s` | Interactive session list |
| `PREFIX $` | Rename session |
| `PREFIX (` / `PREFIX )` | Switch to previous/next session |

### Windows

| Key | Action |
|---|---|
| `PREFIX c` | New window |
| `PREFIX ,` | Rename window |
| `PREFIX n` / `PREFIX p` | Next / previous window |
| `PREFIX [0-9]` | Go to window by number |
| `PREFIX w` | Visual window list |
| `PREFIX f` | Search windows by text |
| `PREFIX &` | Close window |

### Panes

| Key | Action |
|---|---|
| `PREFIX "` | Split top/bottom |
| `PREFIX %` | Split left/right |
| `PREFIX o` | Cycle panes |
| `PREFIX ←↑↓→` | Move to pane by direction |
| `PREFIX z` | Zoom / unzoom pane |
| `PREFIX !` | Pop pane into its own window |
| `PREFIX :join-pane -s <session>:<window>` | Bring window in as a pane |
| `PREFIX x` | Close pane |

### Copy Mode

| Key | Action |
|---|---|
| `PREFIX [` | Enter copy mode |
| `v` | Begin selection (vi mode) |
| `y` | Copy selection |
| `PREFIX ]` | Paste buffer |
| `PREFIX :capture-pane` | Copy entire visible pane |
| `PREFIX :list-buffers` | Show paste buffer stack |
| `PREFIX :choose-buffer` | Pick buffer to paste |

### Useful Commands

```bash
PREFIX :source-file ~/.tmux.conf   # reload config
PREFIX :pipe-pane -o "cat >> ~/session.log"  # log pane output
PREFIX ?                           # show all key bindings
```

---

## Book Notes

Notes from [tmux 2: Productive Mouse-Free Development](https://pragprog.com/titles/bhtmux2/tmux-2/) (The Pragmatic Programmers).

- [Chapter 1 - Learning the Basics](basics.md)
- [Chapter 2 - Configuring tmux](configuration.md)
- [Chapter 3 - Scripting Customized tmux Environments](scripting.md)
- [Chapter 4 - Working with Text and Buffers](buffers.md)
- [Chapter 5 - Pair Programming with tmux](pair-programming.md)
- [Chapter 6 - Workflows](workflows.md)

---

## Resources

- [tmux on GitHub](https://github.com/tmux/tmux) - source, releases, changelog
- [tmux man page](https://man7.org/linux/man-pages/man1/tmux.1.html) - full reference
- [TPM - tmux Plugin Manager](https://github.com/tmux-plugins/tpm) - manage plugins with `PREFIX I` to install
- [tmux-resurrect](https://github.com/tmux-plugins/tmux-resurrect) - save and restore sessions across reboots (`PREFIX Ctrl-s` / `PREFIX Ctrl-r`)
- [tmux-continuum](https://github.com/tmux-plugins/tmux-continuum) - automatic saving via tmux-resurrect
- [vim-tmux-navigator](https://github.com/christoomey/vim-tmux-navigator) - seamless pane navigation between vim and tmux
- [Oh My Tmux](https://github.com/gpakosz/.tmux) - well-maintained `.tmux.conf` starter config
