# Git

[:octicons-arrow-left-24:{ .icon } Back](index.md) | [Detailed Guide](../git/index.md)

Distributed version control. Three areas: working tree -> staging area -> repository.

### Installation & Config

```bash
sudo apt install git

git config --global user.name "Your Name"
git config --global user.email "you@example.com"
git config --global core.editor vim
git config --global init.defaultBranch main
git config --global pull.rebase true
```

Edit `~/.gitconfig` for aliases:

```ini
[alias]
    st  = status -sb
    lg  = log --graph --oneline --decorate --all
    co  = checkout
    sw  = switch
    rb  = rebase
    cp  = cherry-pick
    pu  = push -u origin HEAD
```

### Core Concepts

| Area | Description |
|---|---|
| Working tree | files on disk |
| Staging (index) | what goes into the next commit |
| Repository | `.git` history |
| HEAD | pointer to current branch or commit |
| Remote | copy of repo on a server (e.g. origin) |

### Quick Reference

```bash
# Init and clone
git init
git clone https://github.com/user/repo.git
git clone --depth 1 url              # shallow clone (no full history)

# Stage and commit
git status -sb
git add file.txt
git add -p                           # stage hunks interactively
git diff --staged                    # review what is staged
git commit -m "message"
git commit --amend --no-edit         # amend last commit (unpushed only)

# Branches
git branch -a                        # list all branches including remote
git switch -c feature                # create and switch (modern syntax)
git checkout -b feature              # same, older syntax
git merge feature
git merge --no-ff feature            # preserve merge commit
git branch -d feature                # delete merged branch
git branch -D feature                # force delete

# Remote
git remote -v
git fetch origin
git pull --rebase origin main
git push -u origin feature
git push --force-with-lease          # safer than --force
```

### Common Workflows

#### Feature branch

```bash
git switch -c feature/my-feature
# make changes
git add -p
git commit -m "feat: add my feature"
git push -u origin feature/my-feature
# open PR, then after merge:
git switch main && git pull
git branch -d feature/my-feature
```

#### Interactive rebase - clean up commits

```bash
git rebase -i HEAD~3                 # squash/edit last 3 commits
git rebase -i origin/main            # rebase onto upstream
# pick, squash (s), fixup (f), reword (r), drop (d)
```

#### Stash - save dirty state

```bash
git stash
git stash push -m "wip: half-done refactor"
git stash list
git stash pop                        # apply top stash and drop
git stash apply stash@{1}            # apply without dropping
git stash drop stash@{0}
```

### Undoing Things

```bash
git restore file.txt                 # discard working tree change
git restore --staged file.txt        # unstage file
git reset HEAD~1                     # undo last commit, keep changes staged
git reset --soft HEAD~1              # undo last commit, keep changes in working tree
git reset --hard HEAD~1              # undo last commit, discard all changes
git revert abc1234                   # new commit that undoes a commit (safe for shared branches)
git clean -fd                        # delete untracked files and directories
```

### Advanced

```bash
# Cherry-pick a commit from another branch
git cherry-pick abc1234
git cherry-pick abc1234..def5678     # range

# Find which commit introduced a bug
git bisect start
git bisect bad                       # current is broken
git bisect good v1.0                 # last known good tag
git bisect run ./test.sh             # automate with a test script
git bisect reset

# Recover lost commits
git reflog
git switch -c recovery abc1234

# Search history
git log -S "function_name"           # commits that added/removed string
git log -G "regex"                   # commits where diff matches regex
git log --follow -- file             # history across renames
git log --since="2 weeks ago"

# Patch workflow
git format-patch origin/main         # generate patch files
git apply changes.patch
git am *.patch                       # apply with commit metadata

# Show who changed each line
git blame -L 10,20 file.txt
```

### Tips

- Use `--force-with-lease` instead of `--force` - it fails if remote changed
- `.gitignore` ignores untracked files; `.git/info/exclude` is local-only
- `git add -p` stages hunks interactively - great for focused commits
- Commit messages: imperative mood, 50 char subject, blank line before body
- `git log --all --oneline --graph` gives a visual branch overview

### See Also

- [Personal git notes](../git/index.md)
- Also: lazygit (TUI for git), gh (GitHub CLI), delta (syntax-highlighted diffs)
