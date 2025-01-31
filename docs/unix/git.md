# Git

 [:octicons-arrow-left-24:{ .icon } Back](index.md) | [Detailed Guide](../git/index.md)

### Installation

Install Git:

````bash
apt-get install git
````

### Configuration

Edit: `~/.gitconfig`

````ini
[user]  
    name = smk  
    email = smk@minetest.in  
[alias]  
    st = status -sb  
    lg = log --graph --abbrev-commit --decorate  
[core]  
    editor = vim  
````

### Common Workflows

Clone a repository

````bash
git clone https://github.com/user/repo.git
````

Create and push branch

````bash
git checkout -b feature  
git add .  
git commit -m "Add feature"  
git push -u origin feature  
````

### Pro Tips

1. **Rebase**: Squash commits with `git rebase -i HEAD~3`.
2. **Stash**: Temporarily save changes with `git stash`.
3. **Reflog**: Recover lost commits via `git reflog`.

### See Also

* [giteveryday(7)](https://man.freebsd.org/cgi/man.cgi?query=giteveryday)