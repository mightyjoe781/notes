# fzf

 [:octicons-arrow-left-24:{ .icon } Back](index.md)

A command-line fuzzy finder for filtering and selecting files, commands, and more.

### Installation

````bash
sudo apt install fzf  # Debian/Ubuntu
brew install fzf      # macOS
````

### Basic Usage

* Basic Files

````bash
fzf
````

* Search Command History

```bash
history | fzf
```

* Search and open files

````bash
vim $(fzf)
````

### Advanced Features

#### Preview Files

````bash
fzf --preview 'cat {}'
````

#### Multi-Select

````bash
fzf --multi
````

#### Integration with `cd`

````bash
cd $(find . -type d | fzf)
````

#### Other

* Use `Ctrl+T` to insert selected files into the command line
* Bind `fzf` to `Ctrl+R` for interactive history search

#### Example ZSH Functions

````bash
#!/usr/local/env zsh

# Open file
# fe [FUZZY PATTERN] - Open the selected file with the default editor
#   - Bypass fuzzy finder if there's only one match (--select-1)
#   - Exit if there's no match (--exit-0)
function fe {
  local files
  IFS=$'\n' files=($(fzf --query="$1" --multi --select-1 --exit-0))
  [[ -n "$files" ]] && ${EDITOR:-vim} "${files[@]}"
}

# fcd - cd to selected directory
function fcd {
  local dir
  dir=$(fd . "${1:-.}" --type=d | fzf --no-multi --layout=reverse --height=40%) &&
  cd "$dir"
}

# fcda - including hidden directories
function fcda {
  local dir
  dir=$(fd . "${1:-.}" --hidden --type=d | fzf --no-multi --layout=reverse --height=40%) &&
  cd "$dir"
}

# cdf - cd into the directory of the selected file
function cdf {
  local file
  local dir
  file=$(fzf --query "$1" --no-multi --layout=reverse --height=40%) && dir=$(dirname "$file") && cd "$dir"
}


# Tmux
function fta {
  local session
  session=$(tmux list-sessions -F "#{session_name}" | \
    fzf --layout=reverse --height=20% --query="$1" --select-1 --exit-0) &&
  tmux -CC attach -d -t "$session"
}
````

### Resources

* https://thevaluable.dev/practical-guide-fzf-example/
