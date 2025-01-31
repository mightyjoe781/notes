# Bash/Zsh Shell Configuration

 [:octicons-arrow-left-24:{ .icon } Back](index.md) 

### Optimize terminal workflow

Installation (if required)

````bash
# Install Zsh  
sudo apt install zsh  

# Set Zsh as default shell  
chsh -s $(which zsh)  
````

### Configuration

Edit `~/.bashrc` or `~/.zshrc`

````bash
# Aliases
alias ll='ls -alh'
alias grep='grep --color=auto'

# Prompt customization
PS1='\[\033[1;32m\]\u@\h:\w\$ \[\033[0m\]'

# History settings
HISTSIZE=5000
HISTTIMEFORMAT="%F %T "
````

Apply Changes

````bash
source ~/.bashrc # or source ~/.zshrc
````

### Key Features

|  Command   |        Description        |
| :--------: | :-----------------------: |
|    `!!`    |    Rerun last command     |
|    `!$`    | last argument or prev cmd |
| `ctrl + r` |      search history       |
|   `cd -`   |    previous directory     |

#### Pro Tips

* Use `stow` to manage dotfiles:

````bash
mkdir ~/dotfiles && cd ~/dotfiles  
stow -t ~/ bash  
````

* Enable **autocompletion**

````bash
sudo apt install bash-completion
````

### smk’s dotfiles

````bash
# get the files
git clone https://github.com/mightyjoe781/.dotfiles

cd ~/.dotfiles
# validate install files, its a stow on array of folders

./install
````

