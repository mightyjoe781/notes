#!/usr/bin/env python3
"""Generate site/llms.txt from docs/ frontmatter after `mkdocs build`.

Walks docs/<topic>/, reads each note's `title`/`description` frontmatter,
and emits an https://llmstxt.org/-style index grouped by topic. Run this
after `mkdocs build` (see deploy.sh) so it lands in site/ untouched by
MkDocs' HTML rendering.
"""

import os
import re
import sys

import yaml

DOCS_DIR = "docs"
SITE_URL = "https://notes.sudomoon.com/"
OUTPUT_PATH = "site/llms.txt"

SKIP_DIRS = {"assets", "src", "tmp", ".obsidian", "excalidraw_library"}


def should_skip_dir(name: str) -> bool:
    return name in SKIP_DIRS or name.startswith("Excalidraw")


FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---\n", re.DOTALL)


def read_frontmatter(path: str) -> dict:
    with open(path, encoding="utf-8", errors="ignore") as f:
        text = f.read()
    match = FRONTMATTER_RE.match(text)
    if not match:
        return {}
    try:
        data = yaml.safe_load(match.group(1))
    except yaml.YAMLError:
        return {}
    return data if isinstance(data, dict) else {}


def url_for(rel_path: str) -> str:
    """docs/go/lego/ch1.md -> https://.../go/lego/ch1/ (index.md -> folder root)."""
    rel_path = rel_path[:-3]  # strip .md
    if rel_path.endswith("/index"):
        rel_path = rel_path[: -len("index")]
    else:
        rel_path += "/"
    return SITE_URL + rel_path


def collect_sections():
    sections = {}
    for topic in sorted(os.listdir(DOCS_DIR)):
        topic_path = os.path.join(DOCS_DIR, topic)
        if not os.path.isdir(topic_path) or should_skip_dir(topic):
            continue

        entries = []
        section_title = topic
        for root, dirs, files in os.walk(topic_path):
            dirs[:] = sorted(d for d in dirs if not should_skip_dir(d))
            for fname in sorted(files):
                if not fname.endswith(".md") or fname.endswith(".excalidraw.md"):
                    continue
                fpath = os.path.join(root, fname)
                rel = os.path.relpath(fpath, DOCS_DIR)
                fm = read_frontmatter(fpath)
                title = fm.get("title") or os.path.splitext(fname)[0].replace("_", " ").title()
                description = fm.get("description", "")
                tags = fm.get("tags") or []

                if fname == "index.md" and root == topic_path:
                    section_title = title
                    continue  # topic hub becomes the section header, not a list entry

                if "index" in tags and fname == "index.md":
                    # sub-folder hub page: still list it, it's a useful entry point
                    pass

                entries.append((title, url_for(rel), description))

        if entries:
            sections[section_title] = entries
    return sections


def render(sections: dict) -> str:
    lines = ["# smk's notes", "", "> Personal reference wiki covering software engineering, systems, and tools.", ""]
    for section_title, entries in sections.items():
        lines.append(f"## {section_title}")
        for title, url, description in entries:
            if description:
                lines.append(f"- [{title}]({url}): {description}")
            else:
                lines.append(f"- [{title}]({url})")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def main():
    if not os.path.isdir(DOCS_DIR):
        print("docs/ not found, run from repo root", file=sys.stderr)
        sys.exit(1)

    sections = collect_sections()
    output = render(sections)

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write(output)

    total_entries = sum(len(v) for v in sections.values())
    print(f"Wrote {OUTPUT_PATH}: {len(sections)} sections, {total_entries} entries")


if __name__ == "__main__":
    main()
