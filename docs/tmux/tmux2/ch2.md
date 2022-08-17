## Chapter 2 : Configuring Tmux

#### Introducing the `.tmux.conf` File

By default there are two places where these files are sourced from

- `/etc/tmux.conf` or `$HOME/.tmux.conf`

If one doesn’t exists then create one.

- To source conf file `PREFIX :source-file ~/.tmux.conf`

Example `.tmux.conf`

````.tmux.conf
# setting the prefix from C-b to C-a
set -g prefix C-a

# Free the original Ctrl-b prefix keybinding 
unbind C-b

# setting the delay beteween prefix and command
set -s escape-time 1

# Set the base index for windows to 1 instead of 0
set -g base-index 1

# set the base index for panes to 1 instead of 0
set -g pane-base-index 1
````

#### Customizing Keys, Commands, and User Input

````.tmux.conf
# reload the file with Prefix r
bind r source-file ~/.tmux.conf

# NOTE : -n prefix tells tmux that no need to require prefix
bind-key -n C-r source-file ~/.tmux.conf

# Ensure that we can send Ctrl-A to other apps
# usually we reuquire that in vim, emacs, etc.
bind C-a send-prefix

# screen style pane splitting with | and ~
bind | split-window -h
bind - split-window -v

# remapping movement keys
bind h select-pane -L
bind j select-pane -D
bind k select-pane -U
bind l select-pane -R

# Quick window selection
bind -r C-h select-window -t :-
bind -r C-l select-window -t :+

# pane resizing with prefix H,J,K,L (vim style)
# -r (allows one hit of prefix and then multiple hit of command )
bind -r H resize-pane -L 5
bind -r J resize-pane -D 5
bind -r K resize-pane -U 5
bind -r L resize-pane -R 5

# mouse support - set to on if you want to use mouse
set -g mouse off

````



#### Visual Styling 

On Mac : set `xterm-256color`. check using `tput colors`

On Linux : `[ -z "$TMUX" ] && export TERM=xterm-256color `Add this to `.bashrc`

````.tmux.conf
# set the default terminal mode to 256color mode
set -g default-terminal "screen-256color"
````

To find the appropriate color for you use this bash script

````bash
for i in {0..255} ; do
	printf "\x1b[38;5;${i}m${i}] "
done
````

**Making Customization**

````.tmux.conf
# set the status line's colors
set -g status-style fg=white,bg=black

# set the color of the window lsit
setw -g window-status-style fg=cyan,bg=black

# set colors for active winodw 
setw -g window-status-current-style fg=white,bold,bg=red

# colors for pane borders
setw -g pane-border-style fg=green,bg=black
setw -g pane-active-border-style fg=white,bg=yellow

# active pane normal, other shaded out
setw -g window-style fg=colour240;bg=colour235
setw -g window-active-style fg=white,bg=black

# Command / mesage line
set -g message-style fs=white,bold,bg=black
````

#### Customizing the Status Line‘s Content

| Variable         | Description                                |
| ---------------- | ------------------------------------------ |
| #H               | Hostname                                   |
| #h               | Hostname of local host without domain name |
| #F               | current window flag                        |
| #l               | current windwo index                       |
| #P               | current pane index                         |
| #S               | current session name                       |
| #T               | current window title                       |
| #W               | current window name                        |
| ##               | a literal #                                |
| #{shell-command} | First line of shell command                |
| #[attributes]    | color/attribute change                     |



````.tmux.conf
# Status line left side to show Session:window:pane
set -g status-left-length 40
set -g status-left "#[fg=green]Session: #S #[fg=yellow]#I #[fg=cyan]#P"


# Status line right side -  31-Oct 13:37
set -g status-right "#[fg=cyan]%d %b %R"

# update the status line every sixty seconds
set -g status-interval 60

# center the window list in status line
set -g status-justify centre

# enable activity alerts
setw -g monitor activity on
set -g visual-activity on
````

