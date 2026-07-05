---
title: jq
description: Cheatsheet for jq, the command-line JSON processor - selecting, filtering, restructuring, and shell integration.
tags:
  - reference
---
# jq

[:octicons-arrow-left-24:{ .icon } Back](index.md)

Command-line JSON processor. Useful for pretty-printing, filtering, and reshaping JSON from APIs or files.

### Installation

```bash
sudo apt install jq        # Debian/Ubuntu
brew install jq            # macOS
```

### Common Flags

| Flag | Description |
|---|---|
| `-r` | raw output (strips quotes from strings) |
| `-c` | compact output (single line) |
| `-n` | no input (use `null` as input) |
| `-e` | exit non-zero if output is `false`/`null` |
| `-s` | slurp all inputs into one array |
| `--arg k v` | bind shell variable as `$k` in filter |

---

### Pretty Print

```bash
cat data.json | jq '.'
curl -s api.example.com/users | jq '.'
```

---

### Select Keys

Assumes `data.json`:

```json
{"name": "Alice", "age": 30, "address": {"city": "NYC", "zip": "10001"}}
```

```bash
jq '.name'           # "Alice"
jq '.age'            # 30
jq -r '.name'        # Alice      (no quotes)
jq '.address.city'   # "NYC"
```

---

### Arrays

Assumes `todos.json` is an array of `{id, title, completed}` objects.

```bash
# unpack all elements (stream objects one by one)
jq '.[]' todos.json

# index
jq '.[0]'            # first item
jq '.[-1]'           # last item

# slice (inclusive start, exclusive end)
jq '.[2:4]'          # items at index 2 and 3, returns array
jq '.[-2:]'          # last 2 items, returns array

# pick a field from one element
jq '.[4].title'      # "Buy milk"
```

---

### Pipe and Multiple Outputs

```bash
# comma = multiple outputs from same input
jq '.[4] | .title, .id'
# "Buy groceries"
# 5

# pipe inside jq - apply filter to each element
jq '.[] | .title'
# "Task one"
# "Task two"
# ...

# combine fields per object (no staggering)
jq '.[] | {title, id}'
# {"title": "Task one", "id": 1}
# {"title": "Task two", "id": 2}
```

---

### Restructure JSON

```bash
# rename keys
jq '.[] | {todo: .title, done: .completed}'
# {"todo": "Buy milk", "done": false}

# add a new key
jq '.[] | .points = 2'

# string interpolation
jq -r '.[] | "Task \(.id): \(.title)"'
# Task 1: Buy milk
# Task 2: Read book
```

---

### Built-in Functions

```bash
# keys of an object
jq 'keys'                    # ["age", "name", "address"]

# length - array length or string length
jq 'length'                  # 200  (if array)
jq '.name | length'          # 5

# sort and reverse
jq '[.[] | .id] | sort'
jq '[.[] | .id] | reverse'

# unique
jq '[.[] | .status] | unique'

# map - apply to every element
jq 'map(.id += 1)'           # increment all ids
jq 'map(.title += " [done]")' # append to all titles

# select - filter by condition
jq '.[] | select(.completed == true)'
jq '.[] | select(.id >= 197)'
jq '.[] | select(.id > 10 and .id < 20)'

# min/max by field
jq 'min_by(.id)'
jq 'max_by(.id)'

# group by field
jq 'group_by(.completed)'
```

---

### Control Flow

```bash
# if-then-else
jq '.[] | if .completed then .title else empty end'

# assign based on condition
jq '.[] | .priority = if .id % 2 == 0 then "high" else "low" end'

# output:
# {"id": 1, "title": "Task one", "completed": false, "priority": "low"}
# {"id": 2, "title": "Task two", "completed": true,  "priority": "high"}
```

---

### Shell Integration

```bash
# pass shell variable into filter
name="Alice"
jq --arg n "$name" '.[] | select(.name == $n)' users.json

# extract value into shell variable
city=$(jq -r '.address.city' data.json)

# pipe curl output directly
curl -s https://api.example.com/todos | jq '.[] | select(.completed == false) | .title'
```

---

### Tips

- `.[]` streams objects individually; `.[2:4]` returns an array - mixing these up causes weird output
- Use `-r` when piping jq output to other commands (removes surrounding quotes)
- `..` recursively unpacks all values - useful for exploring unknown JSON structure
- `empty` in a filter drops that element from output entirely

### See Also

- `jq` manual: `man jq` or [jq docs](https://jqlang.org/manual/)
- [curl](curl.md) - often paired for API calls
