# tldr

 [:octicons-arrow-left-24:{ .icon } Back](index.md)

Simplified man pages for quick reference

### Installation

````bash
sudo apt install tldr
# brew install tldr
````

### Basic Usage

````bash
tldr tar
# tldr fzf
````

````bash
tldr tldr	# understand usecases of tldr
````

### Example Uses

* with fzf

````bash
tldr --list | fzf | xargs tldr  # open fzf menu with all tldr cmds
````

* get a random command

````bash
tldr --list | shuf -n1 | xargs tldr  
````