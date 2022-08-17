## Chapter 3 : Scripting Customized Tmux Environments

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



