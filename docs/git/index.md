# Git

Git is a distributed version control system that tracks changes to files over time. Every clone is a full copy of the repository, including its entire history.

```bash
git init                          # start tracking a directory
git clone <url>                   # copy a remote repo locally
git status                        # see what changed
git log --oneline --graph --all   # visualize branch history
```

## Why Git?

- **Distributed** - every clone is a full backup; no single point of failure
- **Fast** - most operations are local with no network required
- **Safe** - nothing is truly lost; reflog records every HEAD movement
- **Standard** - virtually every team and CI/CD tool expects Git

## Topics

| #   | Topic                        | What you will learn                                               |
| --- | ---------------------------- | ----------------------------------------------------------------- |
| 1   | [Internals](internals.md)    | Object store, blobs, trees, commits, tags, OIDs, the DAG          |
| 2   | [Branches](branches.md)      | Creating branches, HEAD, detached HEAD, merge vs rebase           |
| 3   | [Remotes](remotes.md)        | clone, fetch, pull, push, upstream configuration                  |
| 4   | [History](history.md)        | log, diff, interactive rebase, cherry-pick, reflog, bisect, blame |
| 5   | [Worktrees](worktrees.md)    | Multiple working directories without stashing                     |
| 6   | [Submodules](submodules.md)  | Vendoring dependencies, subtrees, sparse checkout, partial clone  |
| 7   | [Hooks and Config](hooks.md) | Automation, aliases, Git LFS, gitconfig                           |
| 8   | [Modern Git](modern.md)      | New features from Git 2.23 to 2.45+                               |

## Quick Reference

```bash
# First-time setup
git config --global user.name "Your Name"
git config --global user.email "you@example.com"
git config --global init.defaultBranch main

# Daily workflow
git status                        # what changed
git add <file>                    # stage a file
git add -p                        # stage interactively (hunk by hunk)
git commit -m "message"           # commit staged changes
git push                          # push to remote

# Branching
git switch -c feature             # create and switch to a new branch
git switch main                   # switch to an existing branch
git merge feature                 # merge into the current branch
git branch -d feature             # delete a merged branch

# Inspecting
git log --oneline --graph --all   # visual history of all branches
git diff                          # unstaged changes
git diff --staged                 # staged changes
git show <commit>                 # inspect a single commit

# Undoing
git restore <file>                # discard unstaged changes
git restore --staged <file>       # unstage a file
git revert <commit>               # safe undo via a new commit
git stash                         # temporarily shelve changes
git stash pop                     # restore the latest stash
```

## Resources

- [Official Documentation](https://git-scm.com/doc)
- [Pro Git Book (free)](https://git-scm.com/book/en/v2)
- [Git Pocket Guide](https://www.oreilly.com/library/view/git-pocket-guide/9781449327507/)
- [Oh Shit, Git!](https://ohshitgit.com/)
