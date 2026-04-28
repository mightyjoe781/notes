# Modern Git

Notable features added from Git 2.23 onward, grouped by theme.

## Ergonomics

### git switch and git restore (2.23)

`git checkout` handled too many unrelated tasks. Two focused commands replaced it.

```bash
# git switch - for branch operations
git switch main                       # switch to an existing branch
git switch -c feature                 # create and switch to a new branch
git switch -d abc123                  # detached HEAD at a specific commit
git switch -                          # switch to the previous branch

# git restore - for file operations
git restore file.txt                  # discard unstaged changes in a file
git restore --staged file.txt         # unstage a file
git restore --source HEAD~2 file.txt  # restore a file from 2 commits ago
git restore --source feature file.txt # restore a file from another branch
```

### Push Auto-Setup (2.37)

Automatically set the upstream tracking branch on the first push, so you never need `-u origin <branch>` again.

```bash
git config --global push.autoSetupRemote true
```

### SSH Commit Signing (2.34)

Sign commits with an SSH key as an alternative to GPG. No keyring or web of trust required.

```bash
git config --global gpg.format ssh
git config --global user.signingkey ~/.ssh/id_ed25519.pub
git config --global commit.gpgsign true

git log --show-signature              # verify signatures in the log
```

### Fixup and Autosquash

Commit a targeted fix, then let rebase automatically squash it in the right place.

```bash
git commit --fixup=<commit>           # creates "fixup! <original message>"
git rebase -i --autosquash main       # Git orders and squashes fixups automatically
```

Set `rebase.autoSquash = true` in your gitconfig to apply autosquash by default.

## Performance

### git maintenance (2.29)

Runs background housekeeping (commit-graph updates, packing, pruning) on a schedule.

```bash
git maintenance start                 # register repo and start scheduled tasks
git maintenance run                   # run all tasks once
git maintenance run --task=gc         # run one specific task
git maintenance stop                  # stop scheduled maintenance
```

Available tasks: `gc`, `commit-graph`, `prefetch`, `loose-objects`, `incremental-repack`, `pack-refs`.

### Commit Graph (2.18+, improved through 2.34)

A precomputed index of the commit DAG. Speeds up `git log`, reachability checks, and `git merge-base` significantly on large repos.

```bash
git commit-graph write --reachable    # build or update the graph
git config core.commitGraph true      # read it automatically
```

`git maintenance start` keeps the commit graph updated automatically.

### Scalar (2.38)

A wrapper that enables all large-repo performance features in one command: partial clone, sparse checkout, commit-graph, filesystem monitor, and scheduled maintenance.

```bash
scalar clone <url>                    # clone with all performance features
scalar register                       # apply to an existing repo
scalar unregister                     # stop managing a repo
```

Scalar was developed by Microsoft for the Windows and Office monorepos and contributed to Git core.

### Filesystem Monitor (2.37 native integration)

Watches for file changes at the OS level so Git does not need to stat every file on `git status`. Makes status and add much faster in large working trees.

```bash
git config core.fsmonitor true
git config core.untrackedCache true
```

## Cloning at Scale

### Partial Clone (2.22+)

Download only the object types you need; Git fetches missing objects on demand.

```bash
git clone --filter=blob:none <url>    # no file blobs (fastest for sparse checkout)
git clone --filter=tree:0 <url>       # no trees or blobs (commit graph only)
```

All standard Git commands work transparently; missing objects are fetched automatically.

### Bundle URI (2.39)

Servers can advertise a CDN URL containing a pre-packaged bundle of the repo. Clients download the bulk from the CDN and fetch only the recent delta from the server, dramatically reducing initial clone time for large repos. This is transparent to the client once configured server-side.

## History and Merging

### rerere - Record and Reuse Resolved Conflicts

`rerere` records how you resolve conflicts and replays the same resolution automatically the next time the same conflict appears.

```bash
git config rerere.enabled true

# After enabling, resolve conflicts normally.
# Git records the resolution automatically.

git rerere diff                       # show the recorded resolution
git rerere forget path/to/file        # discard a specific recording
```

Particularly useful when rebasing a long-running branch onto main repeatedly.

### git log --remerge-diff (2.36)

Shows the actual change a merge commit introduced compared to both parents. Useful for understanding what a merge did without looking at individual commits.

```bash
git log --remerge-diff -1 <merge-commit>
```

## Security

### SHA-256 Repositories (2.29)

Create a repo that uses SHA-256 instead of SHA-1 for object IDs. Produces 64-character OIDs.

```bash
git init --object-format=sha256
git clone --object-format=sha256 <url>
```

Interoperability with SHA-1 repos is limited. Most hosted services (GitHub, GitLab) do not yet support SHA-256 repos as of 2025; adoption is gradual.
