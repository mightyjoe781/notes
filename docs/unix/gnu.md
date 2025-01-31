# GNU Coreutils

 [:octicons-arrow-left-24:{ .icon } Back](index.md) 

Master file/text manipulation and system basics.

### Installation

Preinstalled on most Linux systems. Verify/update:

````bash
sudo apt update && sudo apt install coreutils
````

### Essential Commands

| Category | Command                     | Description                   |
| -------- | --------------------------- | ----------------------------- |
| File Ops | `cp -a`                     | archive-preserving copy       |
|          | `mv -i`                     | interactive rename (prompt)   |
|          | `rm -I`                     | Safe bulk delete (1 prompt)   |
| Text     | `grep -C 3 'text'`          | show 3 lines around match     |
|          | `sed -i 's/old/new/g' file` | in-place replace              |
|          | `awk '{print $1}'`          | print first column            |
| System   | `df -h`                     | Human-readable disk space     |
|          | `du -sh *`                  | directory sizes summary       |
| Search   | `find . -mtime -7`          | files modified in last 7 days |
|          | `locate -i pattern`         | case-insensitive file search  |
|          |                             |                               |

### Advanced Usage

* Bulk rename with `xargs` and `sed`:

````bash
ls *.txt | xargs -I {} sh -c 'mv {} $(echo {} | sed "s/.txt/.md/")'
````

* parallel processing with `parallel`

````bash
find . -name "*.log" | parallel -j 4 gzip
````

* Compare Directories

````bash
diff -qr dir1/ dir2/
````

### Configuration

Customize `ls` color `~/.bashrc`

````bash
export LS_COLORS="di=1;36:ln=35:*.zip=32"
alias ls="ls --color=auto"
````

Safe defaults `~/.bash_aliases`

````bash
alias cp="cp -i --preserve=all"  
alias rm="rm -I"  
````

#### Pro Tips

* **Dry Run** for destructive operations

````bash
rm -Iv *  # Interactive verbose
cp -anv src/ dest/  # No-clobber dry-run
````

* Timing command Executions

```bash
time grep -r "pattern" /large_dir  
```

* Split large files

````bash
split -b 100M bigfile.zip "bigfile_part_"  
````

### Troubleshooting

| Issues                     | Solution                                   |
| -------------------------- | ------------------------------------------ |
| "Permission denied"        | Use `sudo` or `chmod/chown`                |
| "Argument list too long"   | Use `xargs`: `find ... | xargs rm`         |
| Special chars in filenames | Use quotes or escape: `rm 'file$name.txt'` |
|                            |                                            |

#### See also

* `man coreutils`
* `info coreutils`
* [Coreutils Manual](https://www.gnu.org/software/coreutils/manual/)