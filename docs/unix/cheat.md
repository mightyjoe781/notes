# cheat.sh

 [:octicons-arrow-left-24:{ .icon } Back](index.md)

Instant answers for commands, programming, and more

### What is cheat.sh ?

`cheat.sh` is a command-line cheat sheet that provides quick answers for

* Linux Commands (e.g. `tar`, `grep`, `awk`)
* Programming Languages (e.g. `Python`, `JavaScript`, `Go`)
* Tools (e.g. `Git`, `Docker`, `Kubernetes`)

It is accessible via `curl` or a browser, making it a go-to resource for quick help.

### Installation

No installation needed! Use `curl` to access it

````bash
curl cheat.sh
````

For a better experience, install the `cht.sh` wrapper

````bash
curl https://cht.sh/:cht.sh > ~/bin/cht.sh
chmod +x ~/bin/cht.sh
````

### Basic Usage

#### 1. Query a Command

````bash
curl cheat.sh/tar

# or to find a word
curl cheat.sh/tar | grep -C 3 "contents"
````

#### 2. Search for a Topic

````bash
curl cheat.sh/python/list+comprehension
````

3. #### Use the wrapper

With `cht.sh`, queries are simpler

````bash
cht.sh tar
cht.sh python list comprehension
````

### Examples

| Query Type         | Command                      | Output Description             |
| ------------------ | ---------------------------- | ------------------------------ |
| **Linux Commands** | `curl cheat.sh/grep`         | Examples of `grep` usage       |
| **Programming**    | `curl cheat.sh/python/split` | Python `str.split()` examples  |
| **Tools**          | `curl cheat.sh/git`          | Common Git commands            |
| **Error Messages** | `curl cheat.sh/curl+error+7` | Explanation for `curl error 7` |

#### Advanced Features

* Inline Queries: Use `:` to query directly in the terminal

````bash
cht.sh :help
cht.sh :list
````

* Multiple Queries: Combine Topics for detailed answers

```bash
cht.sh python+json+load
```

* Local Caching: Enable caching for faster responses

````bash
export CHEATSH_CACHE=~/.cheat.sh
mkdir -p $CHEATSH_CACHE
````

* Syntax Highlighting: Use `bat` or `pygmentize` for colored output

````bash
curl cheat.sh/python/functions | bat
````

### Integration with Editors

* Vim Integration

````bash
:nmap \c :!curl cheat.sh/<cword><CR>  
````

* VS Code: Install the `cheat.sh` plugin for quick access.

### Tmux Based cht.sh

````bash
#!/usr/bin/env bash

# put your languages, and chat commands in following files
selected=`cat ~/.tmux-cht-languages ~/.tmux-cht-command | fzf`
if [[ -z $selected ]]; then
    exit 0
fi

read -p "Enter Query: " query

if grep -qs "$selected" ~/.tmux-cht-languages; then
    query=`echo $query | tr ' ' '+'`
    tmux neww bash -c "echo \"curl cht.sh/$selected/$query/\" & curl cht.sh/$selected/$query & while [ : ]; do sleep 1; done"
else
    tmux neww bash -c "curl -s cht.sh/$selected~$query | less"
fi
````

