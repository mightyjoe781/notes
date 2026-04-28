# Remotes

A remote is a named reference to another Git repository, usually hosted on GitHub, GitLab, Bitbucket, or a self-hosted server.

## Cloning

Cloning creates a local copy and automatically configures `origin` as the remote.

```bash
git clone <url>                        # clone into a directory named after the repo
git clone <url> mydir                  # clone into a specific directory
git clone --depth 1 <url>             # shallow clone (latest snapshot only, no full history)
git clone --filter=blob:none <url>    # partial clone (omit file blobs, fetch on demand)
git clone --branch v2.0 <url>        # clone and check out a specific branch or tag
```

## Remote Management

```bash
git remote -v                          # list all remotes with their URLs
git remote add upstream <url>          # add a second remote named 'upstream'
git remote set-url origin <url>        # change the URL of a remote
git remote rename origin src           # rename a remote
git remote remove upstream             # remove a remote
```

A repository can have multiple remotes. The most common setup for open-source contribution:

```
origin    <- your fork
upstream  <- the original repository
```

## fetch vs pull

`git fetch` downloads new data but does not touch your working tree.
`git pull` is `git fetch` followed by a merge (or rebase if configured).

```bash
git fetch origin                       # download from origin without merging
git fetch --all                        # fetch every configured remote
git fetch origin feature               # fetch a specific remote branch

git pull                               # fetch + merge
git pull --rebase                      # fetch + rebase (produces cleaner linear history)
git pull origin main                   # pull a specific branch
```

Prefer `git fetch` when you want to inspect changes before integrating them:

```bash
git fetch origin
git log HEAD..origin/main              # commits on remote not in your local branch
git log origin/main..HEAD              # commits you have locally that are not on remote
git diff origin/main                   # diff between your branch and remote
```

## Pushing

```bash
git push                               # push current branch to its upstream
git push origin feature                # push a specific local branch
git push -u origin feature             # push and set upstream tracking
git push --force-with-lease            # safer force push (see below)
git push origin --delete feature       # delete a remote branch
git push origin v1.0                   # push a tag
git push origin --tags                 # push all tags
```

### Force Push

A regular `--force` overwrites the remote branch unconditionally. Use `--force-with-lease` instead: it refuses to push if the remote has commits you have not fetched yet, preventing accidental overwrite of others' work.

```bash
git push --force-with-lease            # safe force push
git push --force-with-lease=main:abc123  # also check a specific OID
```

Avoid force-pushing to shared branches (`main`, `develop`). Only force-push to branches you own.

## Syncing a Fork

```bash
git remote add upstream https://github.com/original/repo.git
git fetch upstream
git rebase upstream/main               # rebase your local main onto the upstream
git push origin main                   # update your fork
```

## Viewing Remote State

```bash
git remote show origin                 # detailed info: URLs, tracking branches, fetch/push config
git ls-remote origin                   # list all refs on the remote (branches, tags, PRs)
```
