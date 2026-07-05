# smk's notes

Personal MkDocs Material knowledge base, published at https://notes.sudomoon.com/.
Source is `docs/<topic>/`, one folder per topic, each with an `index.md` hub.

## Topics (`docs/`)

Run `ls docs/` for the current topic list - one folder per topic, each with an
`index.md` hub. Ignore `assets`, `src`, `tmp`, `Excalidraw*`, `.obsidian` - non-content.

A few folder names aren't self-explanatory:
- `mt` - Luanti (Minetest)
- `sd` - System design (HLD/LLD)
- `other_sde` - Misc SDE topics that don't fit elsewhere

## Navigation

- Invoked from repo root with no folder given: run `ls docs/` to see current
  topics, pick the right `docs/<topic>/`, then work inside it. Don't grep/read
  across all of `docs/` unscoped.
- Inside a topic, start at its `index.md` (the hub), then grep for what you need
  (e.g. `grep -rl "tags:.*draft" docs/<topic>/`) rather than reading every file.
  This is one example, not a rule to only touch drafts - grep for whatever the
  task actually needs (a term, a tag, a filename) and read/edit any relevant
  file, draft or not.
- Files with frontmatter carry a one-line `description`. When narrowing down
  which file(s) in a topic are relevant, scan descriptions first -
  `grep -A2 '^title:' docs/<topic>/**/*.md` or `grep '^description:'` across
  the folder - before falling back to full-text grep or reading whole files.
  It's a cheap filter and usually enough to decide what's worth opening. Not
  all notes have frontmatter yet (see below), so fall back to full-text grep
  for those.
- `collect.py` bundles a topic into `split/` for pasting into external LLM UIs.
  It is not a search shortcut for you - reading the bundle wastes more context
  than grepping the folder directly.

## Frontmatter

```yaml
title: Two Pointer
description: One-sentence summary of what the note covers.
tags:
  - reference   # or: concept, or: index
  - draft         # remove once reviewed
```
`reference` = scan for quick lookup. `concept` = needs full read to rebuild
understanding - most algorithm/technique write-ups with worked examples and
reasoning belong here, not `reference`. `index` = a hub/navigation page (like
a folder's `index.md`) that's just a list of links, not content to read.
`draft` = unreviewed, drop the tag once it's solid. An extra cross-topic tag
is fine when a note genuinely spans topics beyond its own folder - not the
default, just not banned.

`title` and `description` help both MkDocs search and Claude: before grepping
or reading full files across a topic, scan each file's `description` first to
judge relevance - it's cheaper than opening the file and usually enough to
decide whether a full read is worth it.

## See Also

```markdown
## See Also
- [Goroutines](../concurrency/goroutines.md)
```
3-5 links max, added only while already editing that note for another reason.
Never a standalone backfill pass across many files.

## Style

- Short hyphens (-) only in note content, never em dashes (—).

## Session convention

- Scope each session to one folder and one kind of edit (e.g. "tag `docs/go/`",
  not "improve my notes").
- Commit at the end of the session - git log is the record of what was done,
  not chat history. Do not add a "Co-Authored-By: Claude" trailer to commits
  in this repo.
- Treat edits as proposals: review the diff before considering a note done.

## Lint

`vale docs/` is available (custom + Microsoft style, see `.vale.ini`) but
rarely used - optional, not part of the standard workflow.
