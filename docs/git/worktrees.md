# Worktrees

Git Worktrees let you check out multiple branches simultaneously into separate directories, all sharing one `.git` database.

- **Traditional Git**: 1 repository, 1 working folder, 1 active branch
- **Git Worktree**: 1 repository, multiple folders, multiple active branches

When you fetch in one worktree, the new data is immediately available in all others because they share the same history and object store.

## When to Use Worktrees

- Reviewing a PR while keeping your current feature branch untouched
- Running a long build or test suite on one branch while working on another
- Comparing the behaviour of two branches side-by-side
- Maintaining a `release` branch alongside active development

## Setup: Standard Clone

The simplest approach. Clone normally and add worktrees as needed.

```bash
git clone <url> project
cd project

# Add a worktree for an existing remote branch
git worktree add ../project-feature feature/login

# Add a worktree and create a new branch
git worktree add -b hotfix ../project-hotfix main

# List all worktrees
git worktree list

# Remove a worktree when done (the branch is not deleted)
git worktree remove ../project-feature
```

## Setup: Bare Clone

A bare clone contains only the Git data with no working tree. It is visually cleaner for a permanent worktree setup.

```bash
# Recommended layout:
# project/
# +-- repo.git/       <- bare repo (Git data only)
# +-- main/           <- worktree for main
# +-- feature-login/  <- worktree for a feature branch

mkdir project && cd project

git clone --bare <url> repo.git

cd repo.git

# Bare clones do not configure remote refs correctly by default
git config remote.origin.fetch "+refs/heads/*:refs/remotes/origin/*"
git fetch origin

# Add worktrees
git worktree add ../main main
git worktree add ../feature-login feature/login
```

## Tracking and Detached HEAD

If a worktree ends up in detached HEAD state (common with non-nested paths), fix it:

```bash
cd feature-login
git checkout feature/login        # re-attach HEAD to the branch

# Point tracking to a different upstream
git branch -u origin/feature/v2
```

## Constraints

- You cannot check out the same branch in two worktrees at the same time
- If `main` is already checked out and you try to open a `review` worktree pointing to `main`, Git will refuse

Workaround: create a local branch `_main` (or any other name) at the same commit. Use that in the review worktree to inspect the latest state without conflicting with the `main` worktree.

## Naming Conventions

Prefer descriptive folder names that reflect the purpose rather than the branch name. The folder is what you navigate to every day; branch names can be long and include slashes.

| Folder | Branch |
|--------|--------|
| `project-review` | `feature/long-branch-name-v2` |
| `project-hotfix` | `hotfix/payment-rounding` |
| `project-main` | `main` |

## References

- [Git Worktree: Managing Multiple Working Directories](https://www.meziantou.net/git-worktree-managing-multiple-working-directories.htm)
- [git-worktree official docs](https://git-scm.com/docs/git-worktree)
