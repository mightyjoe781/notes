# Bash/Zsh

[:octicons-arrow-left-24:{ .icon } Back](index.md)

A shell is a command interpreter and scripting language. Bash is the default on most Linux systems; Zsh is the default on macOS. Most syntax is compatible between them.

### Installation

```bash
sudo apt install zsh
chsh -s $(which zsh)        # set as default shell
source ~/.zshrc             # reload config
```

### Config Files

| File | Runs when |
|---|---|
| `~/.bashrc` | every interactive non-login bash shell |
| `~/.bash_profile` | bash login shells (SSH, terminal app) |
| `~/.zshrc` | every interactive zsh shell |
| `~/.profile` | login shells (POSIX fallback) |

### Key Shortcuts

| Shortcut | Action |
|---|---|
| `Ctrl+r` | reverse search history |
| `Ctrl+a` / `Ctrl+e` | jump to start / end of line |
| `Ctrl+w` | delete word backwards |
| `Ctrl+u` | delete to beginning of line |
| `Ctrl+l` | clear screen |
| `Alt+.` | paste last argument of previous command |
| `!!` | repeat last command |
| `!$` | last argument of last command |
| `!*` | all arguments of last command |
| `cd -` | switch to previous directory |

### Variables & Expansion

```bash
NAME="world"
echo "Hello $NAME"              # Hello world
echo ${NAME^^}                  # WORLD (uppercase)
echo ${NAME:-default}           # use default if NAME is unset
echo ${NAME:+set}               # "set" only if NAME has a value
echo ${#NAME}                   # string length: 5
echo ${NAME:0:3}                # substring: wor

# Command substitution
today=$(date +%F)
lines=$(wc -l < file.txt)

# Arithmetic
echo $((2 + 3 * 4))
x=5; ((x++)); echo $x           # 6
```

### Conditionals

```bash
# File tests
if [[ -f file.txt ]]; then echo "file exists"; fi
if [[ -d /tmp ]]; then echo "directory"; fi
if [[ -z "$VAR" ]]; then echo "empty string"; fi
if [[ -n "$VAR" ]]; then echo "non-empty string"; fi
if [[ -x script.sh ]]; then echo "executable"; fi

# String comparison
[[ "$a" == "$b" ]]
[[ "$a" != "$b" ]]
[[ "$a" =~ ^prefix ]]           # regex match (no quotes around regex)

# Numeric comparison
[[ $n -gt 10 ]]                 # greater than
[[ $n -le 5 ]]                  # less than or equal
(( n > 10 ))                    # arithmetic test (alternative)

# Combine
[[ -f file && -r file ]]        # AND
[[ -z "$a" || -z "$b" ]]        # OR
```

### Loops

```bash
# Range
for i in {1..5}; do echo $i; done
for i in {0..20..5}; do echo $i; done   # step by 5

# Array
items=(apple banana cherry)
for item in "${items[@]}"; do echo "$item"; done
echo "${#items[@]}"             # array length

# C-style
for ((i=0; i<5; i++)); do echo $i; done

# While - read file line by line
while IFS= read -r line; do
    echo "$line"
done < file.txt

# Until
until [[ -f /tmp/ready ]]; do sleep 1; done
```

### Functions

```bash
greet() {
    local name="${1:-World}"    # local scoping, default value
    echo "Hello, $name"
    return 0
}
greet "Alice"

# Capture output
result=$(greet "Bob")
```

### Pipelines & Redirection

```bash
cmd > file.txt              # stdout to file (overwrite)
cmd >> file.txt             # stdout append
cmd 2> err.txt              # stderr to file
cmd 2>&1                    # stderr to stdout
cmd &> file.txt             # both stdout and stderr to file
cmd < file.txt              # stdin from file
cmd1 | cmd2                 # pipe stdout to stdin
cmd1 | tee file.txt | cmd2  # branch: write to file AND pipe forward
```

### Common Patterns

```bash
# Fail fast in scripts
set -euo pipefail

# Run on each file
find . -name "*.log" | xargs rm -f
find . -name "*.txt" -exec wc -l {} \;

# Process substitution (no temp file needed)
diff <(sort file1) <(sort file2)

# Conditional execution
make && ./bin/app
[[ -f config.yaml ]] || cp config.yaml.example config.yaml

# Bulk rename
for f in *.txt; do mv "$f" "${f%.txt}.md"; done

# Here string
grep "pattern" <<< "some text to search"

# Generate sequence
seq 1 10
seq 0 0.1 1.0
```

### Configuration

```bash
# ~/.zshrc or ~/.bashrc

# Aliases
alias ll='ls -lah'
alias gs='git status'
alias ..='cd ..'
alias ...='cd ../..'

# History
HISTSIZE=10000
SAVEHIST=10000
setopt HIST_IGNORE_DUPS         # Zsh: skip duplicates
HISTCONTROL=ignoredups          # Bash: skip duplicates

# Prompt (Bash)
PS1='\[\033[1;32m\]\u@\h \[\033[1;34m\]\w\[\033[0m\]\$ '
```

### Tips

- Always quote variables `"$var"` to prevent word splitting on spaces
- Use `[[ ]]` instead of `[ ]` - it is safer and supports `=~` and `&&`/`||`
- Use `local` inside functions to avoid polluting global scope
- `shellcheck` lints scripts and catches common bugs
- `set -euo pipefail` at the top of scripts: exit on error, unset vars, pipe failures

### See Also

- [Tmux](tmux.md), [Vim](../vim/index.md)
- Also: fish (friendlier defaults), starship (cross-shell prompt), zoxide (smarter `cd`), direnv (per-directory env vars), stow (dotfile manager)
