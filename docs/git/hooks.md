# Hooks and Config

## Git Configuration

Git config is layered. Settings at a narrower scope override broader ones.

| Scope | File | Applies to |
|-------|------|-----------|
| System | `/etc/gitconfig` | All users on the machine |
| Global | `~/.gitconfig` | Your user account |
| Local | `.git/config` | This repository only |
| Worktree | `.git/config.worktree` | This worktree only |

```bash
git config --list --show-origin     # show all config values and where they come from
git config --global user.name "Name"
git config --global user.email "you@example.com"
git config --global core.editor "vim"
git config --global init.defaultBranch main
```

### Recommended Global Config

```ini
[user]
    name = Your Name
    email = you@example.com

[core]
    editor = vim
    autocrlf = input            # convert CRLF to LF on commit (Linux/Mac)

[alias]
    st = status -sb
    lg = log --oneline --graph --all --decorate
    undo = reset HEAD~1 --mixed
    aliases = config --get-regexp alias

[pull]
    rebase = true               # use rebase instead of merge on pull

[push]
    autoSetupRemote = true      # auto-set upstream on first push (Git 2.37+)

[rebase]
    autoSquash = true           # auto-apply fixup! and squash! commits
```

### Aliases

```bash
git config --global alias.st "status -sb"
git config --global alias.lg "log --oneline --graph --all --decorate"
git config --global alias.undo "reset HEAD~1 --mixed"
```

## Hooks

Hooks are scripts in `.git/hooks/` that Git runs at specific lifecycle points. They are not committed or cloned by default.

To share hooks with your team, store them in a tracked directory and configure Git to use it:

```bash
mkdir .githooks
git config core.hooksPath .githooks
git add .githooks
```

### Common Hooks

| Hook | When it runs | Common use |
|------|-------------|-----------|
| `pre-commit` | Before a commit is recorded | Lint, format, check for secrets |
| `commit-msg` | After writing the commit message | Enforce message format (e.g. Conventional Commits) |
| `pre-push` | Before pushing to a remote | Run tests |
| `post-checkout` | After switching branches | Install deps, notify tooling |
| `pre-rebase` | Before a rebase starts | Warn or block on certain branches |
| `post-merge` | After a successful merge | Install new deps |

### Example: pre-commit Hook

```bash
#!/bin/sh
# .githooks/pre-commit

npm run lint --silent
if [ $? -ne 0 ]; then
    echo "Lint failed. Fix errors before committing."
    exit 1
fi
```

```bash
chmod +x .githooks/pre-commit
```

A non-zero exit code from any hook aborts the Git operation.

### Hook Managers

For team projects, a hook manager is more reliable than raw scripts:

| Tool | Best for |
|------|----------|
| [Husky](https://typicode.github.io/husky/) | Node.js projects |
| [pre-commit](https://pre-commit.com/) | Python or language-agnostic projects |
| [Lefthook](https://github.com/evilmartians/lefthook) | Fast, no runtime dependency |

## Git LFS

Large File Storage moves large binary files (images, videos, model weights, datasets) out of the Git object store into a separate backend. The repo stores lightweight pointers instead.

### Setup

```bash
git lfs install                     # one-time setup per machine

git lfs track "*.psd"               # track by extension
git lfs track "data/*.parquet"      # track by path pattern

git add .gitattributes              # commit the tracking rules
git commit -m "track large files with LFS"
```

### Daily Use

After setup, use normal Git commands. LFS is transparent.

```bash
git add design.psd
git commit -m "add design file"
git push                            # LFS files upload to the LFS backend
```

```bash
git lfs ls-files                    # list tracked files
git lfs status                      # LFS status
git lfs pull                        # download LFS files explicitly
git lfs migrate import --include="*.psd"  # migrate existing history to LFS
```

### When to Use LFS

Use LFS for files that are large, binary, and do not need line-level diffs: design assets, compiled binaries, audio/video, ML model weights, and large datasets. For dependencies, use a package manager instead.
