# ripgrep (rg)

[:octicons-arrow-left-24:{ .icon } Back](index.md)

Fast alternative to `grep`. Respects `.gitignore` by default, skips binary files, searches recursively, and supports PCRE2 regex.

### Installation

```bash
sudo apt install ripgrep     # Debian/Ubuntu
brew install ripgrep         # macOS
```

### Basic Usage

```bash
rg "pattern"                 # search current directory recursively
rg "pattern" src/            # search specific directory
rg "pattern" file.txt        # search specific file
rg -i "pattern"              # case-insensitive
rg -w "word"                 # whole word match
rg -v "pattern"              # invert match (lines NOT matching)
rg -c "pattern"              # count matching lines per file
rg -l "pattern"              # list matching files only
rg -L "pattern"              # list files with NO match
rg -e "pat1" -e "pat2"       # multiple patterns (OR)
rg -F "literal.text"         # treat pattern as literal string
```

### Flags Reference

| Flag | Description |
|---|---|
| `-i` | case-insensitive |
| `-w` | whole word |
| `-v` | invert match |
| `-c` | count matches per file |
| `-l` | list files only |
| `-L` | list files with no match |
| `-n` / `-N` | show / hide line numbers |
| `-A n` | n lines after match |
| `-B n` | n lines before match |
| `-C n` | n lines context (before and after) |
| `-t TYPE` | search only this filetype (py, js, go, rust) |
| `-T TYPE` | exclude filetype |
| `-g GLOB` | include files matching glob |
| `-g '!GLOB'` | exclude files matching glob |
| `-U` | multiline mode |
| `-P` | PCRE2 regex (lookahead, backreference) |
| `-F` | fixed string (no regex) |
| `--json` | JSON output |
| `-r REPLACE` | replace matches in output |
| `--hidden` | search hidden files (dotfiles) |
| `--no-ignore` | ignore .gitignore rules |
| `-0` | null-delimited output (for xargs) |

### Common Patterns

```bash
# Context around match
rg -C 3 "TODO" src/

# Search only Python files
rg "def " -t py

# Search and replace output (does not edit files)
rg "foo" -r "bar" src/

# Exclude directory
rg "pattern" -g '!vendor/'
rg "pattern" -g '!{vendor,node_modules}/'

# Search hidden files too
rg --hidden "API_KEY"

# Find TODOs across repo
rg "TODO|FIXME|HACK" --heading

# Multiline match (PCRE2)
rg -U -P "func \w+\(.*?\)" src/

# Output only the matching part
rg -o "[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}" access.log

# Count total matches (not files)
rg -c "error" logs/ | awk -F: '{sum+=$2} END {print sum}'

# Null-separated file list for xargs
rg -l0 "pattern" | xargs -0 sed -i 's/old/new/g'

# Search compressed files (combine with zcat)
zcat app.log.gz | rg "ERROR"
```

### Integration with fzf

```bash
# Interactive search with preview
rg --color=always "pattern" | fzf --ansi

# Live grep in fzf (search as you type)
rg --color=always -l "" | fzf --preview 'rg --color=always {q} {}'
```

### .ripgreprc

Create `~/.ripgreprc` to set defaults:

```
# Always search hidden files
--hidden

# Ignore common dirs
--glob=!.git
--glob=!node_modules
--glob=!vendor

# Smart case (case-insensitive if all lowercase)
--smart-case
```

```bash
export RIPGREP_CONFIG_PATH=~/.ripgreprc
```

### See Also

- [fzf](fzf.md) for interactive fuzzy matching
- Also: grep (POSIX standard), ag (the silver searcher), ack
