# Git Worktrees

Git Worktrees is standard way to handle *context switching* without the friction of stashing or rebuilding.

While IDE can switch branches in a single folder, it cannot show two branches side-by-side or prevent cache invalidation like a worktree can.

Generally switching the branch in a repo requires you to stash your local changes or commit them, but lets say you are not interested in doing that at the moment, or let's say your job requires you to review a lot of PRs reviews, or context switch to different branches, its always better to use git worktrees. You don't need to rebuild project multiple times.

- Traditional Git : 1 Repository ~ 1 Working Folder ~ 1 Active Branch
- Git Worktree : 1 Repository ~ Multiple Folders ~ multiple active branches

All folder will share the same `.git` database, If you fetch in one folder, the new data is instantly available in all others because they share same history and object store.

There are two ways to set it up.

- Using default clones repos
- Using bare repos (just a little visually cleaner solution)

I would suggest to not use `--bare` flag at all if you are new to git worktrees,
Rather clone simply the repo and don't update `refs`.

```bash

# Assume we have a project `starship` for example

starship/
├── repo.git/         # Bare repository (Git data only)
├── main/             # Worktree for main branch
├── feature-v1/       # Worktree for feature branch
└── feature/gui       # Worktree for new feature branch

mkdir starship
cd starship

## clone a bare repo, and renamed it to repo.git rather than .bare for consistency
# naming to .git conflicts from git spaces and causes confusion
git clone --bare <repo-url> repo.git

# creating a worktree
cd repo.git

# fix remote refs as bare doesn't have them correctly setup
# git clone by default does these two steps, side effect of --bare
git config remote.origin.fetch '+refs/heads/*:refs/remotes/origin/*'
git fetch origin


git worktree add ../main

# let's say we have feature branch v1 or gui
# -t helps with set up the tracking
git worktree add ../feature-v1 feature/v1 # non-nested, need to be fixed for tracking
git worktree add ../feature/gui # nested feature folder, tracks upstream automatically

# list worktrees
git worktree list

# removing a worktree
git worktree remove feature/v1

```

```bash
# common issues

# branch is not set to track upstream correctly if folders are renamed while checkout
# example above feature-v1
# it created the detached HEAD checkout

cd feature-v1
git checkout feature/v1 # often --checkout passed in worktree doesn't work

# if want to track another upstream
git branch -u origin/feature/v2

```
### Naming Conventions and Branch Management

Generally we maintain a dedicated worktree called `review` for code review. Limitation is you can't checkout same branch twice in a worktree environment.

Example let's say we have `main` checkout out, and try to checkout `review` then git will throw and error.

To get around that create a branch called `_main`, allowing to fetch latest changes or references the main branch without conflicting the actual `main` worktree.

Use meaningful names for worktree name rather branch name for complex feature.


References

- https://www.meziantou.net/git-worktree-managing-multiple-working-directories.htm