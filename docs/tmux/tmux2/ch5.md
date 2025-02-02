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