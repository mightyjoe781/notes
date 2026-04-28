# Branches

A branch is a lightweight pointer to a commit. Creating one is instant and costs almost no storage. Git encourages branching heavily.

## The Default Branch

When you initialise a repo, Git creates one branch. The default name is `main` by modern convention (previously `master`).

```bash
git init -b main                  # set default branch name on init
git config --global init.defaultBranch main  # set globally
```

## Creating and Switching

Git 2.23 introduced `git switch` and `git restore` as focused replacements for the overloaded `git checkout`. Prefer them in new workflows.

```bash
# Create a branch
git branch feature                # create without switching
git switch -c feature             # create and switch (preferred)
git checkout -b feature           # older equivalent

# Switch branches
git switch main
git checkout main                 # older equivalent

# Switch to the previous branch
git switch -

# Delete a branch
git branch -d feature             # safe: refuses if branch is unmerged
git branch -D feature             # force delete regardless
```

## HEAD

`HEAD` is a special pointer to your current position in the graph. Normally it points to a branch name, which in turn points to a commit.

```
HEAD -> main -> commit abc123
```

**Detached HEAD** occurs when HEAD points directly to a commit rather than a branch. This happens when you check out a specific commit, a tag, or a remote-tracking branch.

```bash
git checkout abc123               # enters detached HEAD
git switch -d abc123              # same, with the modern command

# Any commits you make in detached HEAD are reachable only via HEAD.
# To keep them, create a branch before switching away:
git switch -c my-experiment
```

## Remote-Tracking Branches

When you clone or fetch, Git creates read-only **remote-tracking branches** that mirror the state of the remote at the time of the last fetch.

```
origin/main     <- remote-tracking (read-only, updated by fetch/pull)
main            <- your local branch
```

```bash
git fetch origin                  # update remote-tracking branches
git branch -r                     # list remote-tracking branches
git branch -a                     # list local and remote-tracking
```

## Upstream Tracking

A local branch can track a remote branch. Tracking is what makes `git push` and `git pull` work without extra arguments.

```bash
git push -u origin feature        # push and set upstream in one step
git branch --set-upstream-to origin/feature feature
git branch -vv                    # show tracking relationships and ahead/behind counts
```

With Git 2.37+, you can set tracking automatically for all new branches:

```bash
git config --global push.autoSetupRemote true
```

## Merge vs Rebase

Both integrate changes from one branch into another. The difference is what the resulting history looks like.

| | Merge | Rebase |
|-|-------|--------|
| History shape | Preserves all commits; adds a merge commit | Rewrites commits onto the new base; linear history |
| Safety on shared branches | Always safe | Never rebase commits others have pulled |
| Typical use | Integrating a completed feature branch | Cleaning up local work before a PR |

```bash
git merge feature                 # merge with a merge commit
git merge --ff-only feature       # only allow fast-forward (no merge commit)
git merge --squash feature        # squash all changes into one staged diff, then commit manually

git rebase main                   # rebase current branch onto main
git rebase -i HEAD~3              # interactively edit the last 3 commits
git rebase --abort                # cancel a rebase in progress
git rebase --continue             # continue after resolving a conflict
```

## Stashing

Stash temporarily shelves changes so you can switch context without committing.

```bash
git stash                         # stash tracked changes
git stash -u                      # also stash untracked files
git stash list                    # list all stashes
git stash pop                     # restore latest stash and remove it
git stash apply stash@{2}         # restore a specific stash without removing it
git stash drop stash@{0}          # delete a stash
git stash branch feature          # create a branch from a stash
```

## Branch Strategies

**GitHub Flow** (simple, good for continuous delivery)

1. Branch from `main`
2. Commit on the feature branch
3. Open a pull request
4. Review, CI, merge to `main`
5. Deploy from `main`

**Gitflow** (structured, good for versioned releases)

- `main` holds production releases
- `develop` is the integration branch
- `feature/*`, `release/*`, `hotfix/*` are short-lived branches
