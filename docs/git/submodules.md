# Submodules and Large Repos

Tools for managing external dependencies inside a repo and for working efficiently with large repositories.

## Submodules

A submodule embeds another Git repository inside yours at a pinned commit. The parent repo stores the submodule URL and the exact commit it should be at.

### Adding a Submodule

```bash
git submodule add <url> path/to/dir
git commit -m "add submodule"
```

This creates a `.gitmodules` file and a special entry in the index that records the pinned commit.

### Cloning a Repo That Has Submodules

```bash
git clone --recurse-submodules <url>

# If you already cloned without the flag:
git submodule update --init --recursive
```

### Updating Submodules

```bash
git submodule update --remote                # pull the latest commit from upstream
git submodule update --remote --merge        # merge changes in
git submodule foreach git pull origin main   # run a command in every submodule
```

### Removing a Submodule

```bash
git submodule deinit path/to/dir
git rm path/to/dir
rm -rf .git/modules/path/to/dir
```

## Subtrees

Git subtree merges another repository into a subdirectory of yours. Contributors do not need to run any extra commands; the subtree is just regular files to them.

```bash
# Add a subtree
git subtree add --prefix lib/util <url> main --squash

# Pull updates from the upstream repo
git subtree pull --prefix lib/util <url> main --squash

# Push changes back upstream
git subtree push --prefix lib/util <url> main
```

### Submodule vs Subtree

| | Submodule | Subtree |
|-|-----------|---------|
| Setup for contributors | Run `submodule update` after every pull | Nothing extra required |
| History | Separate, clean | Merged into parent history |
| Upstream contributions | Easy (separate repo) | Harder (requires subtree push) |
| Use when | Dependency is actively developed separately | Dependency is vendored and rarely changes |

## Sparse Checkout

Check out only a subset of a repository's files. Useful for monorepos where you only need one package.

```bash
git clone --filter=blob:none --sparse <url>
cd repo
git sparse-checkout set path/you/need another/path
```

Managing the set of checked-out paths:

```bash
git sparse-checkout add another/path   # add a path
git sparse-checkout list               # show current patterns
git sparse-checkout disable            # restore full checkout
```

Sparse checkout works with cone mode (recommended: faster, simpler pattern matching):

```bash
git sparse-checkout init --cone
git sparse-checkout set packages/api
```

## Partial Clone

Download only part of the object store on clone; Git fetches missing objects automatically on demand.

```bash
# Fastest: skip all file blobs, fetch content when you check out files
git clone --filter=blob:none <url>

# Most aggressive: skip trees and blobs (commits only)
git clone --filter=tree:0 <url>
```

Partial clones are transparent: all normal Git commands work the same way.

## Large File Storage (LFS)

See [Hooks and Config](hooks.md#git-lfs) for LFS setup. LFS is the right tool when your repo contains large binaries (video, audio, datasets, compiled artifacts) that do not need to be diffed.
