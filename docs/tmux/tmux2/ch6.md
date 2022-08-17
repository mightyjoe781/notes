## Chapter 6 : Workflows

### Working Effectively with Panes and Windows

#### Turning a Pane into a Window

- For popping a pane into a window : `PREFIX !`

#### Turning a Window into a Pane

- We can use `PREFIX :join-pane -s panes:1`  to join first window in a session named panes to current window.

#### Maximizing and Restoring Panes

- We can temporarily make a pane go full screen : `PREFIX z`. It works kinda like toggle switch

#### Launching Commands in Panes

- To access two server in one window with two panes use this script.

````bash
tmux new-session -s servers -d "ssh deploy@burns"
tmux split-window -v "ssh dba@smithers"
tmux atttach -t servers
````

Note there is a handy side that when pipe breaks and server disconnects, panes will autoclose.

#### Opening a Pane in Current Directory

We can use `#{pane_current_path}` provided by tmux for this use.

````.tmux.conf
# split pane and retain the current directory of existing pane
bind _ split-window -v -c "#{pane_current_path}"
bind \ split-window -h -c "#{pane_current_path}"
````

#### Issuing Commands in Many Panes Simultaneously

Using the command `set-window-option synchronize-panes on`, anything you type in one pane will be immediately broadcast to the other panes in the current session.

Then we will need to disabled the broadcast. `set-window-option synchronize-panes off`

Rather than that we can make a toggle binding : `PREFIX CTRL-s`

````.tmux.conf
# shortcut for synchronize-panes toggle
bind C-s set-window-option synchronize-panes
````

### Managing Sessions

#### Moving Between Sessions

Start two session as

````bash
tmux new -s editor -d vim
tmux new -s processes -d top
````

Then connect to editor session : `tmux a -t editor`

To switch session use : `PREFIX (` and `PREFIX )`

To see list of active sessions : `PREFIX s`

````.tmux.conf
bind ( switch-client -p
bind ) switch-client -n
````

#### Moving Windows Between Sessions

- You can use `PREFIX :move-window` or `PREFIX .`, so you can bring up window you want to move, press the key combination and write the name of target session.

#### Creating or Attaching to Existing Session

````bash
if ! tmux has-session -t development; then
	exec tmux new-session -s development -d
	# other setup commands before attaching...
fi
exec tmux attach -t development
````

### Tmux and Your OS

#### Using a Different Shell

````.tmux.conf
set -g default-shell /bin/zsh
````

#### Launching tmux by Default

Add following script block to load tmux by default

````
if [[ -z "$TMUX" ]]; then
	tmux new-session -A -s "$USER"
fi
````

#### Keeping Specific Configuration Separate

Move your OS-specific configuration into a separate file and tell tmux to load it up using tmux’s `if-shell` commands and the `source` command.

```
touch ~/.tmux.mac.conf
```

Add your mac specific stuff in the file above then in main `.tmux.conf` write 

````.tmux.conf
# load mac-specific settings
if-shell "uname | grep -q Darwin" "source-file ~/.tmux.mac.conf"
````

Similarly for loading your secret tmux sauce :)

````.tmux.conf
# load private settings if they exists
if-shell "[ -f ~/.tmux.private ]" "source ~/.tmux.private"
````

#### Recording Program Output to a Log

With pipe-pane, you can toggle it on and off at will and you can start it after a program is already running.

To activate this : `PREFIX :pipe-pane -o "cat >>mylog.txt"`

fix the tmux conf

````.tmux.conf
# log output to a text file on demand
bind P pipe-pane -o "cat >> ~/#W.log" \; display "Toggled logging to ~/#w.log"
````

Now you can use `PREFIX P` to toggle logging in file.

#### Adding Battery Life to Status Line

````bash
wget --no-check-certificate https://raw.github.com/richo/battery/bin/battery
chmod +x ~/batter
# check if its working
~/batter Discharging
````

Adding it to tmux config

````.tmux.conf
# Status line right side - 50% | 31 Oct 13:37
set -g status-right "#(~/battery Discharging) | #[fg=cyan]%d %b %R"
````

#### Integrating Seamlessly with Vim

Install `vim-tmux-navigator` plugin in vim using Plug or Vundle.

Then to easily navigate add this config to your .tmux.conf

````.tmux.conf
is_vim="ps -o state= -o comm= -t '#{pane_tty}' \
 	    | grep -iqE '^[^TXZ ]+ +(\\S+\\/)?g?(view|n?vim?x?)(diff)?$'"
bind-key -n C-h if-shell "$is_vim" "send-keys C-h"  "select-pane -L"
bind-key -n C-j if-shell "$is_vim" "send-keys C-j"  "select-pane -D"
bind-key -n C-k if-shell "$is_vim" "send-keys C-k"  "select-pane -U"
bind-key -n C-l if-shell "$is_vim" "send-keys C-l"  "select-pane -R"
bind-key -n C-\ if-shell "$is_vim" "send-keys C-\\" "select-pane -l"
# Clears screen
bind C-l send-keys 'C-l'
````

### Extending tmux with Plugins

Bruno Sutic developed a solution TPM (tmux plugin manager to deal with the config file problems).

Let’s install `tmux-resurrect` to restore tmux session even after a reboot!!!

```bash
git clone https://github.com/tmux-plugin/tpm ~/.tmux/plugins/tpm
```

Add following Lines to .tmux.conf

````.tmux.conf
set -g @plugin 'tmux-plugins/tpm'
set -g @plugin 'tmux-plugins/tmux-resurrect'
run '~/.tmux/plugins/tpm/tpm'
````

To install plugin `PREFIX I`

To save current tmux window/pane state : `PREFIX CTRL-s`

To restore last state : `PREFIX CTRL-r`