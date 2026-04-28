# History

## Viewing History

```bash
git log                             # full log
git log --oneline                   # compact, one line per commit
git log --oneline --graph --all     # branch graph across all branches
git log -p                          # include the diff for each commit
git log --stat                      # show files changed per commit
git log --author="Name"             # filter by author
git log --since="2 weeks ago"       # filter by date
git log --grep="keyword"            # filter by commit message
git log -- path/to/file             # history of a specific file
git log main..feature               # commits in feature but not in main
git log feature..main               # commits in main but not in feature
```

## Inspecting Changes

```bash
git diff                            # unstaged changes (working tree vs index)
git diff --staged                   # staged changes (index vs last commit)
git diff main..feature              # diff between two branches
git diff HEAD~3..HEAD               # diff over the last 3 commits
git show <commit>                   # show a commit and its diff
git show <commit>:path/to/file      # show the content of a file at a commit
```

## Interactive Rebase

Rewrite, reorder, squash, or drop commits before sharing them. This is the primary tool for cleaning up local work before opening a pull request.

```bash
git rebase -i HEAD~3                # edit the last 3 commits
git rebase -i main                  # edit everything not yet in main
```

Pick actions per commit in the editor:

| Action | Effect |
|--------|--------|
| `pick` | Keep the commit unchanged |
| `reword` | Keep the commit but edit its message |
| `edit` | Pause rebase here to amend the commit |
| `squash` | Merge into the previous commit (combines messages) |
| `fixup` | Merge into the previous commit (discards this message) |
| `drop` | Remove the commit entirely |

**Rule:** Never rebase commits that have been pushed to a shared branch.

### Fixup Workflow

```bash
git commit --fixup=<commit>         # creates a "fixup! <original message>" commit
git rebase -i --autosquash main     # Git automatically orders and squashes fixups
```

Set `rebase.autoSquash = true` in config to always apply autosquash during interactive rebase.

## Cherry-pick

Applies the diff from a specific commit onto the current branch, creating a new commit with a new OID.

```bash
git cherry-pick <commit>            # apply a single commit
git cherry-pick A..B                # apply a range (excludes A)
git cherry-pick A^..B               # apply a range (includes A)
git cherry-pick --no-commit <commit> # apply changes without committing
git cherry-pick --abort             # cancel a cherry-pick in progress
git cherry-pick --continue          # continue after resolving a conflict
```

The original Author is preserved; you become the Committer.

## Reflog

The reflog records every time HEAD moves. It is the safety net for recovering "lost" commits after a bad reset, rebase, or accidental branch deletion.

```bash
git reflog                          # all HEAD movements with timestamps
git reflog show feature             # reflog for a specific branch
git reflog --relative-date          # show human-readable timestamps
```

```bash
# Recover a commit
git reflog                          # find the OID you need
git switch -c recovery abc123       # create a branch at that commit
# or
git reset --hard abc123             # move HEAD back to that commit
```

Reflog entries expire after 90 days by default.

## Bisect

Binary search through commit history to find the first commit that introduced a bug.

```bash
git bisect start
git bisect bad                      # current commit is broken
git bisect good v1.0                # this tag/commit was working

# Git checks out a midpoint commit. Test it manually, then mark it:
git bisect good
# or:
git bisect bad

# Repeat until Git identifies the first bad commit.
git bisect reset                    # return HEAD to where you started
```

Automate with a test script (exit 0 for good, non-zero for bad):

```bash
git bisect run ./test.sh
git bisect run npm test -- --testPathPattern auth.spec
```

## Blame

Shows who last modified each line and in which commit.

```bash
git blame path/to/file              # full blame
git blame -L 10,30 path/to/file     # only lines 10-30
git blame -w path/to/file           # ignore whitespace-only changes
git blame --ignore-rev <commit> path/to/file   # exclude a formatting/whitespace commit
git log -S "function name" -- path/to/file      # find when a string was added or removed
git log -G "regex" -- path/to/file              # find when a line matching a regex changed
```

## Reverting vs Resetting

| Command | What it does | Safe on shared branches? |
|---------|-------------|--------------------------|
| `git revert <commit>` | Creates a new commit that undoes the change | Yes |
| `git reset --soft HEAD~1` | Moves branch pointer back, keeps changes staged | Only if not pushed |
| `git reset --mixed HEAD~1` | Moves branch pointer back, unstages changes | Only if not pushed |
| `git reset --hard HEAD~1` | Moves branch pointer back, discards changes | Only if not pushed |

Use `git revert` on shared branches. Use `git reset` only on local, unpushed commits.
