---
title: grep
description: Cheatsheet for grep - flags, filtering, context lines, and regex patterns for searching plain text.
tags:
  - reference
---
# grep

[:octicons-arrow-left-24:{ .icon } Back](index.md)

Search plain text using patterns. Most commonly used to filter output from other commands via pipe.

### Common Flags

| Flag | Description |
|---|---|
| `-i` | case insensitive |
| `-v` | invert - print lines that do NOT match |
| `-c` | count matches per file |
| `-l` | print only filenames with matches |
| `-n` | print line numbers |
| `-w` | match whole word only |
| `-x` | match whole line only |
| `-r` | recursive search through directories |
| `-e pattern` | explicit pattern (allows searching for `-flag` strings) |
| `-E` | extended regex (ERE) - no need to escape `|`, `+`, `{}` |
| `-A N` | print N lines after each match |
| `-B N` | print N lines before each match |
| `-C N` | print N lines before and after each match |

---

### Basic Usage

```bash
# Search a file directly
grep "DELETE" access.log

# More common - pipe output into grep
cat access.log | grep "DELETE"

# Search all files with an extension
grep "div" *.html
# index.html:  <div class="container">
# index2.html: <div id="main">

# Count matches per file
grep -c "div" *.html
# index.html:12
# index2.html:8
```

---

### Filtering

```bash
# Case insensitive
grep -i "error" app.log

# Invert - lines that do NOT match
grep -v "GET" access.log        # show everything except GET requests

# Whole word match (won't match "division" when searching "div")
grep -w "div" *.html

# Whole line match
grep -x "<html>" *.html
```

---

### Context Lines

Useful when relevant info spans multiple lines (e.g. structured logs).

```bash
# 3 lines after match
grep -A 3 "ERROR" app.log

# 3 lines before match
grep -B 3 "ERROR" app.log

# 3 lines before and after
grep -C 3 "ERROR" app.log
```

---

### Searching for Flags and Special Characters

Grep interprets leading `-` as its own flags:

```bash
# Option 1: double-dash stops flag parsing
man ls | grep -- -a

# Option 2: -e makes the pattern explicit
man ls | grep -e "-a"
```

---

### Regex Patterns

By default grep uses Basic Regex (BRE). Use `-E` for Extended Regex (ERE) to avoid backslash noise.

```bash
# Start of line (^) and end of line ($)
grep "^FROM" Dockerfile          # lines that start with FROM
grep "80$" Dockerfile            # lines that end with 80
grep "^<.*>$" index.html         # lines that are a single HTML tag

# Word boundary (\b) - match at word edge without consuming characters
grep "\bdiv\b" *.html            # matches "div" but not "division"
grep "\b404\b" access.log        # matches 404 but not 2404 or 4040

# OR - two patterns (BRE needs backslash, ERE doesn't)
grep "404\|500" access.log       # BRE
grep -E "404|500" access.log     # ERE - cleaner

# Character ranges
grep -E "[0-9]{3}\.[0-9]{3}" access.log    # match 3-digit.3-digit

# Match all HTTP 4xx errors
grep -E " 4[0-9]{2} " access.log
```

---

### Recursive Search

```bash
# Search all files under a directory
grep -r "TODO" ./src

# With file extension filter
grep -r "TODO" ./src --include="*.py"

# Show only filenames, not matching lines
grep -rl "TODO" ./src
```

---

### Tips

- `grep -v "^#" config.conf | grep -v "^$"` - strip comments and blank lines
- Use `-E` by default to avoid having to escape `|`, `+`, `?`, `{}`
- ripgrep (`rg`) is a faster drop-in replacement with better defaults for code search
- For searching flags in man pages: `man cmd | grep -- -f`

### See Also

- [ripgrep](ripgrep.md) - faster grep with better defaults for code
- [text-processing](text-processing.md) - sed, awk for transforming matched lines
