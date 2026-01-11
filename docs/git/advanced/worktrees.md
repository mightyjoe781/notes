# Git Worktrees

Git Worktrees is standard way to handle *context switching* without the friction of stashing or rebuilding.

While IDE can switch branches in a single folder, it cannot show two branches side-by-side or prevent cache invalidation like a worktree can.

Generally switching the branch in a repo requires you to stash your local changes or commit them, but lets say you are not interested in doing that at the moment, or let's say your job requires you to review a lot of PRs reviews, or context switch to different branches, its always better to use git worktrees. You don't need to rebuild project multiple times.

- Traditional Git : 1 Repository ~ 1 Working Folder ~ 1 Active Branch
- Git Worktree : 1 Repository ~ Multiple Folders ~ multiple active branches

All folder will share the same `.git` database, If you fetch in one folder, the new data is instantly available in all others because they share same history and object store.

```bash

# Assume we have a project `starship` for example

mkdir starship
cd starship

## clone a bare repo, and renamed it to .git rather .bare for consistency
git clone --bare <repo-url> .git

# creating a worktree
git worktree add main

# let's say we have feature branch v1 or gui

git worktree add feature/v1
git worktree add feature/gui

# list worktrees
git worktree list

# removing a worktree
git worktree remove feature/v1

```

### Naming Conventions and Branch Management

Generally we maintain a dedicated worktree called `review` for code review. Limitation is you can't checkout same branch twice in a worktree environment.

Example let's say we have `main` checkout out, and try to checkout `review` then git will throw and error.

To get around that create a branch called `_main`, allowing to fetch latest changes or references the main branch without conflicting the actual `main` worktree.

Use meaningful names for worktree name rather branch name for complex feature.
