# smk's notes

Personal knowledge base built with [MkDocs Material](https://squidfunk.github.io/mkdocs-material/). Live at <https://notes.sudomoon.com/>.

## Structure

```
notes/
├── docs/            # All markdown content + assets (~660 MB)
│   ├── src/         # Custom CSS/JS injected via mkdocs.yml
│   └── toc.md       # Hand-curated table of contents (grid-card layout)
├── overrides/       # Jinja2 template overrides for Material theme
├── split/           # Output of collect.py (topic-split markdown bundles)
├── mkdocs.yml       # Production config
├── mkdocs_local.yml # Local dev config (git-revision plugin disabled)
├── serve.sh         # Local dev server
├── deploy.sh        # Build + rsync to remote server
├── collect.py       # Utility to bundle docs per topic for LLM context
└── setup.txt        # Python venv + pip dependency notes
```

## Setup

```bash
# One-time
virtualenv .venv && source .venv/bin/activate
pip install mkdocs mkdocs-material python-markdown-math mdx_truly_sane_lists \
    pymdown-extensions mkdocs-glightbox pygments \
    mkdocs-git-revision-date-localized-plugin
```

## Local dev

```bash
./serve.sh          # serves on http://127.0.0.1:8000 using mkdocs_local.yml
```

`mkdocs_local.yml` is identical to `mkdocs.yml` except the `git-revision-date-localized` plugin is disabled so hot-reload is fast.

## Deploy

```bash
./deploy.sh         # mkdocs build then rsync site/ → smkroot:/var/www/notes/
```

## MkDocs customizations

### Theme — Material

| Setting | Value |
|---|---|
| Navigation depth | 4 |
| Tabs | enabled |
| Navigation top (back-to-top) | enabled |
| Search suggest + highlight | enabled |
| Code copy button | enabled |

### Template overrides (`overrides/main.html`)

Extends `base.html` to:
- Remove the Prev/Next page buttons (`next_prev` block)
- Remove the search button from the navbar (`search_button` block)
- Redefine the repo link block with FA icon handling

### Custom assets (`docs/src/`)

| File | Purpose |
|---|---|
| `css/custom.css` | Layout / spacing tweaks |
| `css/friendly.css` | Pygments "friendly" syntax highlight palette |
| `css/theme.css` | Colour and font overrides |
| `js/custom.js` | Minor JS enhancements (e.g. MathJax config helpers) |

### Markdown extensions

| Extension | What it enables |
|---|---|
| `admonition` | `!!! note/warning/tip` call-out blocks |
| `mdx_math` + MathJax CDN | Inline `$...$` and block `$$...$$` LaTeX |
| `toc` | Permalink anchor `🔗`, underscore slug separator |
| `mdx_truly_sane_lists` | Sane nested lists (4-space indent) |
| `attr_list` + `md_in_html` + `def_list` | HTML attributes, markdown inside HTML, definition lists |
| `pymdownx.emoji` | Material + Twemoji icon shortcodes (`:material-docker:` etc.) |
| `pymdownx.highlight` | Fenced code blocks with Pygments, line anchors |
| `pymdownx.superfences` | Nested fences, diagram blocks |
| `pymdownx.tasklist` | `- [x]` checkboxes |
| `pymdownx.details` | Collapsible `???` blocks |
| `pymdownx.smartsymbols` | `->`, `(c)` → typographic symbols |
| `glightbox` plugin | Lightbox for images on click |
| `git-revision-date-localized` | "Last updated X ago" footer (prod only) |
| Google Analytics | `G-FSJPS15JWH` via `extra.analytics` |

### Navigation (`nav`)

Only top-level entries are declared in `mkdocs.yml` (`About`, `TOC`). All sub-pages are auto-discovered by MkDocs. The main entry point is `toc.md` which renders a Material grid-card layout with icon shortcuts to every section.

## Repo size note

The `.git` directory is **~205 MB** against **~660 MB** of actual docs — primarily from binary assets (images, PDFs) accumulated across 194 commits. To reduce it:

```bash
brew install git-filter-repo
# Remove blobs > 1 MB from all history
git filter-repo --strip-blobs-bigger-than 1M
git gc --prune=now --aggressive
```

The single largest offender is `media/media/the_pragmatic_programmer_notes.pdf` (14 MB blob). Consider adding large binaries to `.gitignore` or tracking them with Git LFS going forward.

## LLM context utility

`collect.py` bundles the markdown files per topic into split files under `split/`, useful for feeding sections to an LLM:

```bash
python collect.py docs --max-size 0.5   # 0.5 MB chunks per topic
```
