# Text & Data Processing

[:octicons-arrow-left-24:{ .icon } Back](index.md)

Core tools for transforming text, parsing structured data, and processing logs on the command line.

## sed

Stream editor. Reads line by line, applies transformations, outputs result.

```bash
# Substitute
sed 's/old/new/' file.txt           # first match per line
sed 's/old/new/g' file.txt          # all matches (global)
sed -i 's/old/new/g' file.txt       # edit in-place
sed -i.bak 's/old/new/g' file.txt   # in-place with .bak backup

# Delete lines
sed '/pattern/d' file.txt
sed '5d' file.txt                   # delete line 5
sed '3,7d' file.txt                 # delete lines 3 to 7

# Print specific lines
sed -n '5,10p' file.txt             # print lines 5-10 only
sed -n '/start/,/end/p' file.txt    # print between two patterns

# Insert and append
sed '3i\inserted line' file.txt     # insert before line 3
sed '3a\appended line' file.txt     # append after line 3

# Multiple expressions
sed -e 's/foo/bar/' -e 's/baz/qux/' file.txt

# Strip comments and blank lines
sed '/^#/d; /^$/d' config.txt
```

## awk

Pattern-action language. Splits each line into fields; ideal for columnar data.

```bash
# Print columns
awk '{print $1}' file.txt            # first column
awk '{print $1, $3}' file.txt        # columns 1 and 3
awk -F: '{print $1}' /etc/passwd     # colon-delimited

# Filter by pattern
awk '/error/' log.txt                # lines containing "error"
awk '$3 > 100' data.txt              # numeric field filter

# Aggregate
awk '{sum += $1} END {print sum}' numbers.txt
awk 'NR > 1 {print}' file.txt        # skip header (NR = line number)
awk 'END {print NR}' file.txt        # count lines

# Built-in variables
# NR  - current record (line) number
# NF  - number of fields in current record
# FS  - field separator (default: whitespace)
# OFS - output field separator

# Change delimiter in output
awk -F: 'OFS="|" {print $1,$3}' /etc/passwd

# Formatted output
awk '{printf "%-20s %5d\n", $1, $2}' data.txt

# Real-world: top 10 IPs in access log
awk '{print $1}' access.log | sort | uniq -c | sort -rn | head -10

# Compute average
awk '{sum+=$1; count++} END {print sum/count}' numbers.txt
```

## jq

JSON processor for the command line.

```bash
# Install
sudo apt install jq

# Pretty print
cat data.json | jq '.'
jq '.' data.json

# Extract fields
jq '.name' data.json
jq '.users[0]' data.json             # first element
jq '.users[].name' data.json         # name from every element

# Filter
jq '.users[] | select(.age > 18)' data.json
jq '.users[] | select(.active == true) | .email' data.json

# Transform shape
jq '[.users[] | {name, email}]' data.json
jq '.users | length' data.json

# Update and delete
echo '{"a":1}' | jq '.b = 2'         # add field
echo '{"a":1,"b":2}' | jq 'del(.b)'  # remove field
echo '{"n":5}' | jq '.n += 1'         # increment

# Raw string output (no quotes)
jq -r '.name' data.json
curl -s https://api.example.com/users | jq -r '.[].email'

# Compact output
jq -c '.' data.json

# Multiple files
jq '.name' *.json

# Convert array to lines
jq -r '.[]' array.json

# From entries to object
jq 'to_entries | map(.key + "=" + (.value|tostring)) | .[]' obj.json
```

## yq

YAML processor. Same query syntax as jq but works on YAML, JSON, and TOML.

```bash
# Install
sudo wget -qO /usr/local/bin/yq \
  https://github.com/mikefarah/yq/releases/latest/download/yq_linux_amd64
sudo chmod +x /usr/local/bin/yq

# Read
yq '.name' config.yaml
yq '.services.web.image' docker-compose.yaml
yq '.spec.containers[0].image' pod.yaml

# Edit in-place
yq -i '.version = "2.0"' config.yaml
yq -i '.replicas += 1' deployment.yaml

# Convert YAML to JSON
yq -o=json config.yaml

# Convert JSON to YAML
yq -p=json -o=yaml data.json

# Multi-document YAML
yq 'select(.kind == "Deployment") | .metadata.name' k8s-manifest.yaml

# Merge files
yq '. * load("override.yaml")' base.yaml
```

### Tips

- `sed -n '/ERROR/p' app.log` is faster than `grep ERROR app.log` for large files
- `awk 'FNR==NR {a[$1]=$0; next} $1 in a {print a[$1], $0}' f1 f2` joins two files on column 1
- `jq -e` exits with non-zero if the result is false/null - useful in scripts
- `yq` can edit Kubernetes manifests in-place without a full templating engine

### See Also

- [ripgrep](ripgrep.md), [fzf](fzf.md) for interactive search
- Also: miller (`mlr`) for CSV/TSV/JSON pipelines, xsv for fast CSV, xmllint for XML, dasel (like jq for YAML/TOML/JSON/CSV)
