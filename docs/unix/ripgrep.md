# ripgrep

 [:octicons-arrow-left-24:{ .icon } Back](index.md)

A faster, modern alternative to `grep`

### Installation

````bash
sudo apt install ripgrep
# brew install ripgrep
````

### Basic Usage

1. Search in Files

   ````bash
   rg "pattern"
   ````

2. Case-Insensitive Search

   ````bash
   rg -i "pattern"
   ````

3. Search in Specific File Types

   ````bash
   rg "pattern" -t py
   ````

4. Exclude Files/Directories

   ````bash
   rg "pattern" --glob '!node_modules'
   ````

5. JSON Output

   ````bash
   rg "pattern" --json
   ````

6. Replace Text

   ````bash
   rg "old" --replace "new"
   ````

### Combining `rg` with `fzf`

````bash
rg "pattern" | fzf
````

