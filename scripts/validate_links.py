#!/usr/bin/env python3
"""
validate_links.py
Check that all image references in docs/ja/*.md point to files that exist
under docs/public/images/.  Also checks internal markdown links.

Usage: python3 scripts/validate_links.py
"""

import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
DOCS_DIR = REPO_ROOT / "docs"
PUBLIC_IMAGES = DOCS_DIR / "public" / "images"
JA_DIR = DOCS_DIR / "ja"

IMG_RE = re.compile(r"!\[([^\]]*)\]\(([^)]+)\)")
LINK_RE = re.compile(r"\[([^\]]+)\]\((/[^)]+)\)")  # absolute-path internal links

errors: list[str] = []
warnings: list[str] = []


def check_file(md_path: Path):
    text = md_path.read_text(encoding="utf-8")
    rel = md_path.relative_to(REPO_ROOT)

    # Image refs
    for alt, src in IMG_RE.findall(text):
        if src.startswith("http"):
            continue  # external, skip
        # src could be /images/foo.png  or  ../images/foo.png
        if src.startswith("/images/"):
            img_file = PUBLIC_IMAGES / src[len("/images/"):]
        elif src.startswith("/"):
            img_file = DOCS_DIR / "public" / src.lstrip("/")
        else:
            img_file = (md_path.parent / src).resolve()

        if not img_file.exists():
            errors.append(f"{rel}: broken image ref '{src}' (not found at {img_file})")

    # Internal markdown links (absolute paths)
    for text_content, href in LINK_RE.findall(text):
        # strip anchor
        href_path = href.split("#")[0]
        if not href_path:
            continue
        # VitePress resolves from docs root
        candidate = DOCS_DIR / href_path.lstrip("/")
        md_candidate = candidate.with_suffix(".md")
        if not (candidate.exists() or md_candidate.exists()):
            warnings.append(f"{rel}: unresolved link '{href}'")


def main():
    md_files = list(DOCS_DIR.rglob("*.md"))
    print(f"Checking {len(md_files)} markdown files ...\n")

    for f in sorted(md_files):
        check_file(f)

    if warnings:
        print("WARNINGS:")
        for w in warnings:
            print(f"  ⚠  {w}")

    if errors:
        print("\nERRORS:")
        for e in errors:
            print(f"  ✗  {e}")
        print(f"\n{len(errors)} error(s) found.")
        sys.exit(1)
    else:
        print(f"✓ All links OK  ({len(warnings)} warning(s))")


if __name__ == "__main__":
    main()
