# GNU Coreutils

[:octicons-arrow-left-24:{ .icon } Back](index.md)

Standard Unix file, text, and system commands. Preinstalled on all Linux systems.

### File Operations

```bash
# Copy
cp file.txt dest/
cp -r dir/ dest/                     # recursive
cp -a dir/ dest/                     # archive: preserve permissions, timestamps, links
cp -n file.txt dest/                 # no-clobber: skip if dest exists
cp -u file.txt dest/                 # update: skip if dest is newer

# Move / Rename
mv file.txt newname.txt
mv -i file.txt dest/                 # prompt before overwriting

# Remove
rm file.txt
rm -r dir/                           # recursive
rm -i *.log                          # interactive: prompt per file
rm -I dir/                           # one prompt for more than 3 files

# Links
ln -s /path/to/target linkname       # symbolic link
ln /path/to/file hardlink            # hard link
```

### Viewing Files

```bash
cat file.txt
cat -n file.txt                      # show line numbers
less file.txt                        # paginate, searchable with /
head -n 20 file.txt                  # first 20 lines
tail -n 20 file.txt                  # last 20 lines
tail -f /var/log/syslog              # follow (live update)
wc -l file.txt                       # line count
wc -w file.txt                       # word count
```

### Text Processing

```bash
# grep - search
grep "pattern" file.txt
grep -r "pattern" dir/               # recursive
grep -i "pattern" file.txt           # case-insensitive
grep -v "pattern" file.txt           # invert match
grep -n "pattern" file.txt           # show line numbers
grep -c "pattern" file.txt           # count matching lines
grep -l "pattern" *.txt              # list matching files
grep -A 3 -B 3 "pattern" file.txt    # 3 lines context

# sort
sort file.txt
sort -r file.txt                     # reverse
sort -n numbers.txt                  # numeric sort
sort -k2 file.txt                    # sort by column 2
sort -u file.txt                     # unique (deduplicate)

# uniq (must be sorted first)
sort file.txt | uniq
sort file.txt | uniq -c              # count occurrences
sort file.txt | uniq -d              # show duplicates only

# cut - extract columns
cut -d: -f1 /etc/passwd              # first field, colon-delimited
cut -c1-10 file.txt                  # first 10 characters

# tr - translate/delete characters
echo "hello" | tr 'a-z' 'A-Z'
echo "foo  bar" | tr -s ' '          # squeeze repeated spaces
cat file.txt | tr -d '\r'            # remove carriage returns (Windows line endings)

# paste - merge lines
paste file1.txt file2.txt
paste -d, file1.txt file2.txt        # comma-delimited
```

### Search and Find

```bash
find . -name "*.txt"
find . -type f -name "*.log"         # files only
find . -type d                       # directories only
find . -mtime -7                     # modified in last 7 days
find . -size +10M                    # files over 10MB
find . -name "*.log" -exec rm {} \;  # delete found files
find . -name "*.py" | xargs wc -l   # count lines in found files
find . -empty                        # find empty files/dirs

locate filename                      # fast search via index (run updatedb first)
```

### Disk and System

```bash
df -h                                # disk usage of filesystems
du -sh *                             # sizes of items in current dir
du -sh dir/                          # total size of directory
du -h --max-depth=1                  # one-level summary

stat file.txt                        # detailed file metadata
file binary                          # detect file type
which python3                        # full path of command
```

### Process Text with xargs

```bash
# Run command on each line of input
cat files.txt | xargs rm
find . -name "*.bak" | xargs -I {} mv {} /tmp/
echo "file1 file2 file3" | xargs -n 1 echo   # one arg per call

# Parallel execution
find . -name "*.log" | xargs -P 4 gzip       # 4 parallel processes
```

### Safe Defaults

Add to `~/.bash_aliases`:

```bash
alias cp='cp -i'
alias mv='mv -i'
alias rm='rm -I'
alias ls='ls --color=auto'
alias ll='ls -lah'
```

### Tips

- `ls -lah --sort=time` sorts by modification time newest first
- `diff -u file1 file2` shows unified diff (same format as git diff)
- `diff -qr dir1/ dir2/` compares directories recursively
- `split -b 100M bigfile.tar.gz "part_"` splits large files for transfer
- Use `timeout 30 command` to kill a command if it runs longer than 30s

### See Also

- [Text & Data Processing](text-processing.md) for sed, awk, jq
- [ripgrep](ripgrep.md) for faster recursive search
- Also: bat (cat with syntax highlighting), eza (modern ls), fd (faster find)
