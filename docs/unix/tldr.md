---
title: tldr
description: Quick reference for the tldr command, which provides simplified, example-based man pages.
tags:
  - reference
---
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

### See Also

- [cheat.sh](cheat.md) - similar instant-answer tool, also queryable via curl
- [fzf](fzf.md) for interactively picking a command to look up