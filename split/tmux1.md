# Tmux Notes - Part 1
Generated on: 2025-06-01 14:34:33
Topic: tmux
This is part 1 of 1 parts

---

## File: tmux/index.md

# tmux

tmux is a terminal multiplexer which lets you use a single environment to launch multiple terminals, or windows, each running its own process or program.



### Resources

- [Tmux Quick Guide](../unix/tmux.md)
- [Pragmatic Programmer tmux 2nd Edition Notes](tmux2/index.md)



---

## File: tmux/tmux2/ch1.md

# Chapter 1 : Learning the Basics

#### Installation

- mac : `brew install tmux`

- On linux : build from source.

````bash
sudo apt-get install build-essential libevent-dev libncurses-dev
tmux -zxvf tmux-2.6.tar.gz
cd tmux-2.6
./configure
make
sudo make install
````

- On windows : don’t know and won’t try :) jk Use above steps in a WSL environment.

Starting/Exiting Tmux

- To start tmux : `tmux`
- To exit tmux : `exit`
- Creating a named session : `tmux new-session -s basic`
- or shorter version of above command `tmux new -s basic`

#### The Command Prefix

`CTRL-b` is default *command prefix* for tmux which sends signal to tmux to act on keys pressed subsequently rather than the running program in session.

Although it is fine binding but I like to change it to `CTRL-a`. This is default binding on `gnu's screen` (father of tmux).

Try `<C-b>t` : this should display time. 

#### Detaching/Attaching Sessions

- Create a new session : `tmux new -s basic`
- Run an application : `top` or `htop`
- To detach from the tmux session : `PREFIX d`
- To list sessions running : `tmux list-sessions` or `tmux ls`
- For attaching in case of  only one session : `tmux a` or `tmux attach` 
- Create a new session : `tmux new -s second_session -d ` (`-d` flag starts it in detached state)
- Now to attach a specific session : `tmux a -t basic`
- To kill a session : `tmux kill-session -t basic`

#### Working with Windows

- Naming a window shell : `tmux new -s windows -n shell`
- Creating a new window : `PREFIX c`, and execute `top`
- Renaming the window : `PREFIX ,`

**Moving Between Windows**

- To go to next window : `PREFIX n`
- To go to previous window : `PREFIX p`
- To go to nth window : `PREFIX n`
- To display visual menu of window : `PREFIX w`
- To search window that contains some text : `PREFIX f`
- To close a window : `exit` or `PREFIX &`

#### Working with Panes

- To horizontal split panes : `PREFIX %`
- To vertical split panes : `PREFIX "`
- To cycle thru panes : `PREFIX o` or `PREFIX UP/DOWN/LEFT/RIGHT`

**Pane Layouts** 

Default Pane Layouts :  To cycle  : `PREFIX SPACEBAR`

1. even-horizontal
2. even-vertical
3. main-horizontal
4. main-vertical
5. Tiled

**Closing Panes**

`PREFIX x` or `exit`

#### Working with Command Mode

Invoking command mode : `PREFIX :`

Then execute following commands

- `new-window -n console`
- `new-window -n processes "top"` (Note : window will close when you exit top)
- For help `PREFIX ?`

---

## File: tmux/tmux2/ch2.md

# Chapter 2 : Configuring Tmux

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



---

## File: tmux/tmux2/ch3.md

# Chapter 3 : Scripting Customized Tmux Environments

`-t` switch is very useful and can be utlised to streamline our setup of development environment.

- Create a new named session : `tmux new-session -s development -d`
- Create a split window without attaching : `tmux split-window -h -t development`
- Attach to session : `tmux a -t development`
- Attach more splits to window : `tmux split-window -v -t development`

#### Scripting a Project Configuration

Create a script `~/dev` (make sure its executable) and a directory : `~/devproject`

- Create the session : `tmux new-session -s development -n editor -d`
- Add a line to our configuration using `send-keys` : `tmux send-keys -t development 'cd ~/devproject' C-m`

````bash
# create a new-session
tmux new-session -s development -n editor -d

# using send-keys to change cwd
# notice CTRL-m is the way to send <CR> thru sendkey
tmux send-keys -t development 'cd ~/devproject' C-m

# open vim
tmux send-keys -t development 'vim' C-m

# lets split window
# -p %x : to split in x%
tmux split-window -v -t development

# select main-horizontal layout from defaults
tmux select-layout -t development main-horizontal
````

#### Targeting Specific Panes

- Remember our base index in 1 for everything now.
- We can target a pane using `[session]`:`[window]`.`[pane]`
- So to target pane 2 : `development:1.2`

**Creating and Selecting Windows**

````bash
# create a new console pane
tmux new-window -n console -t development
tmux send-keys -t development:2 'cd ~/devproject' C-m

# starting up attached to that window
tmux select-window -t development:1
tmux a -t development
````

Combine both files and try them out. One issue is it creates duplicate sessions , to avoid that use following construct

````bash
tmux has-session -t development
if [ $? != 0 ]
then
	# normal script ^ as above
fil
tmux a -t development
````

#### Using tmux Configuration for Setup

Create a conf file for tmux to start in named `app.conf`

````app.conf
source-file ~/.tmux.conf
# see no need to prefix tmux since its not a bash script
new-session -s development -n editor -d
...
````

Then start tmux as : `tmux -f app.conf attach`

#### Managing Configuration with tmuxinator

tmuxinator is a simple tool you can use to define and manage different tmux-configuration. Window-layout and commands in tmux can be defined in yaml format.

Installing using Rubygems

```bash
gem install tmuxinator
```

tmuxinator need `$EDITOR` variable, make sure its available.

To create a new tmuxinator project : `tmuxinator open development`

Create/Edit the Ruby rails config to this config

````yaml
name: development
root: ~/development
windows:
  - editor:
  		layout: main-horizontal
  		panes:
  			- vim
  			-	# empty, will just run plain bash
  - console: # empty
````

Save and execute : `tmuxinator development`

You could also use  :`tmuxinator debug development` to print actual srcipt being generator by program from yaml.





---

## File: tmux/tmux2/ch4.md

# Chapter 4 : Working with Text And Buffer

#### Scrolling Through Output with Copy Mode

- To enable copy mode : `PREFIX [`
- To enable vi style movement add this line in config

````.tmux.conf
#enable vi keys.
setw -g mode-keys vi
````

#### Moving Quickly Through Buffer

- Utilize vi shortcuts like `g`, or `G` and `CTRL-b` or `CTRL-f`

#### Searching Through Buffer

- Use vi shortcuts like `/{pattern}` or for previous search `?{pattern}`

#### Copying and Pasting Text

- Go in copy mode and press `SPACE` and move cursor to end of line/word you want to copy and hit `ENTER`
- This copies contents into a paste buffer, to print its contents : `PREFIX ]`

#### Capturing a Pane

- To copy entire visible buffer contents : `PREFIX :capture-pane`

#### Showing and saving contents of buffer

- Use : `tmux show-buffer` then to save it `save-buffer buffer.txt`

#### Using Multiple Paster Buffers

By design, tmux stores a stack of paste buffers.

Now try copying multiple line in paste buffers and list buffers : `list-buffers`

By default : `PREFIX ]` always applies paste buffer 0, but we can use `choose-buffer` to select a buffer before pasting its content.

#### Remapping Copy and Paste Keys

Make the binding same as vim

````.tmux.conf
bind Escape copy-mode
bind-key -T copy-mode-vi v send -X begin-selection
bind-key -T copy-mode-vi v send -X copy-selection
unbind p
bind p paste-buffer
````

#### Working with Keyboard on Linux

- Install `xclip` : `sudo apt-get install xclip`

Now add following lines in tmux

````.tmux.conf
# Prefix Ctrl-C takes what's in the buffer and send to system clipboard via xclip
bind C-c run "tmux save-buffer - | xclip -sel clip -i"
````

To invoke it : `PREFIX CTRL-c`

We could also bind it to y key.

````.tmux.conf
# y in copy mode takes selection and send it to system via xclip
bind-key -T copy-mode-vi y send-keys -X copy-pipe-and-cancel "xclip -sel clip -i"
````

To make `PREFIX Ctrl-v` to paste buffers into tmux windows

````.tmux.conf
# prefix Ctrl-v fills tmux buffer from system clipboard via xclip, then pastes from buffer into tmux window
bind C-v run "tmux set-buffer \"$(xclip -sel clip -o)\";tmux paste-buffer"
````

#### Using macOS Clipoboard Commands

In MacOS there is already `pbcopy` and `pbpaste` to work with clipboard.

Inside of tmux you can execute : `tmux show-buffer | pbcopy`

or paste the contents of clipboard : `tmux set -buffer $(pbpaste); tmux paste-buffer`

````.tmux.conf
# Prefix Ctrl-C takes whats in the buffer and sends it to system clipboard via pbcopy
bind C-c run "tmux save-buffer - | pbcopy"

# y in copy mode takes selection and sends it to system clipboard via pbcopy
bind-key -T copy-mode-vi y send-keys -X coyp-pipe-and-cancel "pbcopy"

# prefix ctrl-v fills tmux buffer from clipboard via pbpaste then pastes from buffer into tmux window
bind C-v run "tmux set-buffer \"$(pbpaste)\"; tmux paste-buffer"
````



---

## File: tmux/tmux2/ch5.md

# Chapter 5 : Pair Programming with Tmux

There are two ways to work with remote user

- Create a new account that you share and others share
- uses tmux sockets so you can have a second user connect to your tmux session without having to share your user account

#### Pairing with a Shared Account

- Create a new user : `adduser tmux`

- Add ssh keys

  ````bash
  su tmux
  mkdir ~/.ssh
  touch ~/.ssh/authorized_keys
  chmod 700 ~/.ssh
  chmod 600 ~/.ssh/authorized_keys
  ````

- Each user than would like to connect to tmux user will need public ssh keys

  ````bash
  ssh-keygen
  cat ~/.ssh/id_rsa.pub | ssh tmux@your_server 'cat >> .ssh/authorized_keys'
  # you could also have used ssh-copy-id command but thats alright
  # ssh-copy-id tmux@your_server
  ````

- Then you will have to execute : `tmux new-session -s Pairing`

- Then another team member can login and execute : `tmux attach -t Pairing`

#### Using a Shared Account and Grouped Sessions

- You can create normal session : `tmux new-session -s groupedsession`
- Another person can attach to session in grouped way : `tmux new-session -t groupedsession -s my sesion`

This gives freedom to second user to easily make changes to windows and panes without affecting the first users presentation.

#### Quickly Pairing with tmate

tmat is a fork of tmux designed to make pair programming painless.

Installation : 

````bash
sudo apt-get install software-properties-common
sudo add-apt-repostiory ppa:tmate.io/archive
sudo apt-get update && sudo apt-get install tmate
````

On Mac Installation

```bash
brew install tmate
```

To open tmate : `tmate`

To see console message : `tmate show-messages`

You can copy the `ssh` connection url at the bottom on status line and share it with your pair programmer.

tmate supports the same commands that tmux supports so we can create named sessions and even script it using tmuxinator yaml files.

#### Pairing with Separate Accounts and Sockets

Lets create two users ted and barney

````bash
sudo adduser ted
sudo adduser barney
# create a tmux group and /var/tmux folder that will hold shared session
sudo addgroup tmux
sudo mkdir /var/tmux
# change ownership of above folder such tmux group user can access it
sudo chgrp tmux /var/tmux
# alter permission on folder so its accessible for all member of tmux group
sudo chmod g+ws /var/tmux
sudo usermod -aG tmux ted
sudo usermod -aG tmux barney
````

#### Creating and Sharing Sessions

 Ted creates a session different from default socket : `tmux -S /var/tmux/pairing`

In another window barney executes : `tmux -S /var/tmux/pairing attach`

---

## File: tmux/tmux2/ch6.md

# Chapter 6 : Workflows

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

---

## File: tmux/tmux2/index.md

# Pragmatic Programmer tmux 2nd Edition

- [Chapter 1 : Learning the Basics](ch1.md)
- [Chapter 2 : Configuring Tmux](ch2.md)
- [Chapter 3 : Scripting Customized Tmux Environments](ch3.md)
- [Chapter 4 : Working with Text And Buffer](ch4.md)
- [Chapter 5 : Pair Programming with Tmux](ch5.md)
- [Chapter 6 : Workflows](ch6.md)













---

