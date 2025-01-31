# Tmux

 [:octicons-arrow-left-24:{ .icon } Back](index.md) | [Detailed Guide](../tmux/index.md)

## Installation

````bash
sudo apt install tmux
````

### Configuration

Edit `~/.tmux.conf`

````bash
# Remap prefix to Ctrl-a  
unbind C-b  
set -g prefix C-a  

# Mouse support  
set -g mouse on  

# Split panes  
bind | split-window -h  
bind - split-window -v  

# Status bar  
set -g status-bg cyan  
````

* [Configuration Guide](../tmux/tmux2/ch2/)
* [Example .conf](https://raw.githubusercontent.com/mightyjoe781/.dotfiles/refs/heads/master/tmux/.tmux.conf)

Reload Config

````bash
tmux source-file ~/.tmux.conf
````

### Key Workflows

| Command              | Workflow            |
| -------------------- | ------------------- |
| `tmux new -s <name>` | Start named Session |
| `Ctrl-a d`           | Detach Session      |
| `tmux ls`            | List Session        |
| `Ctrl-a c`           | New Window          |

#### Pro Tips

* Persist sessions with `tmux-resurrect`

````bash
git clone https://github.com/tmux-plugins/tmux-resurrect ~/.tmux/plugins/tmux-resurrect  
````

* Use `ssh-agent` in tmux for shared keys.
* https://tmuxcheatsheet.com/
