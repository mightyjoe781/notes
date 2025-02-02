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