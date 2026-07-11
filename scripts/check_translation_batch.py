#!/usr/bin/env python3
"""
check_translation_batch.py — read-only validation harness for Hacking the Xbox
Japanese translation chapters.

Usage:
    python3 scripts/check_translation_batch.py 13
    python3 scripts/check_translation_batch.py 13 15
    python3 scripts/check_translation_batch.py 13-15
    python3 scripts/check_translation_batch.py all
"""

import re
import sys
import pathlib

# ── repo layout ──────────────────────────────────────────────────────────────
REPO = pathlib.Path(__file__).resolve().parent.parent
DOCS_JA = REPO / "docs" / "ja"
IMAGES_DIR = REPO / "docs" / "public" / "images"
PACKAGE_LOCK = REPO / "package-lock.json"

# ── helpers ──────────────────────────────────────────────────────────────────
MOJIBAKE_RE = re.compile(r"�")
FIGURE_PROSE_RE = re.compile(
    r"(?<!!\[)(?<!\[)\bFigure\s+\d+[-–]\d+",  # Figure N-M not inside []()
    re.IGNORECASE,
)
BARE_URL_KANJI_RE = re.compile(
    r"https?://[^\s\)\]>\"\']+[　-鿿＀-￯]",
)
MARKDOWN_FOOTNOTE_RE = re.compile(r"\[\^")
UNLINKED_CREDIT_URL_RE = re.compile(
    r"(?<!\[)(?<!\()https://takasumasakazu\.net(?!\))"
)
LOCAL_GUIDE_RE = re.compile(
    r"\(/ja/translation-guide\b|\[.*?\]\(/(?:ja/)?translation[-_]guide",
    re.IGNORECASE,
)
DISCOURAGED_TERMS = [
    ("サイドバー", "コラム / 囲み記事"),
    ("アリゲータークリップ", "ワニ口クリップ"),
]
# Patterns that indicate a top credit block (bad if in first 30 lines)
TOP_CREDIT_RE = re.compile(
    r"^\s*\*?(?:原著|   著者|著作権|出版|本翻訳|日本語訳・レビュー)[::：]",
    re.MULTILINE,
)
IMAGE_REF_RE = re.compile(r"!\[.*?\]\(.*?/images/(page-\d{3}-render\.png)\)")


def parse_args(argv):
    """Return sorted list of chapter numbers to check, or None meaning all."""
    args = argv[1:]
    if not args or args == ["all"]:
        return None  # all
    if len(args) == 1:
        m = re.fullmatch(r"(\d+)(?:[-–](\d+))?", args[0])
        if m:
            a, b = int(m.group(1)), int(m.group(2) or m.group(1))
            return list(range(a, b + 1))
    if len(args) == 2:
        try:
            a, b = int(args[0]), int(args[1])
            return list(range(a, b + 1))
        except ValueError:
            pass
    sys.exit(f"Usage: {argv[0]} N | N M | N-M | all")


def find_chapter_files(chapters):
    """Return list of (chapter_num, path) tuples."""
    if chapters is None:
        found = []
        for p in sorted(DOCS_JA.glob("ch*.md")):
            m = re.match(r"ch(\d+)\.md$", p.name)
            if m:
                found.append((int(m.group(1)), p))
        return found
    result = []
    for n in chapters:
        p = DOCS_JA / f"ch{n:02d}.md"
        result.append((n, p))
    return result


def check_chapter(num, path, all_image_files, issues):
    """Run all checks on a single chapter file. Append findings to `issues`."""
    tag = f"ch{num:02d}"

    if not path.exists():
        issues.append((tag, "MISSING", f"File not found: {path}"))
        return set()

    raw = path.read_bytes()
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as e:
        issues.append((tag, "MOJIBAKE", f"UTF-8 decode error: {e}"))
        return set()

    lines = text.splitlines()

    # 1 — mojibake
    for i, line in enumerate(lines, 1):
        if MOJIBAKE_RE.search(line):
            issues.append((tag, "MOJIBAKE", f"Line {i}: replacement char � — {line[:80]}"))

    # 2 — Figure N-M in visible prose (not alt text)
    # Strip image alt text to avoid false positives
    stripped = re.sub(r"!\[.*?\]\([^)]*\)", "", text)
    for m in FIGURE_PROSE_RE.finditer(stripped):
        # get approximate line number
        lineno = text[: m.start()].count("\n") + 1
        issues.append((tag, "FIGURE-LABEL", f"Line ~{lineno}: visible English figure label — {m.group()!r}"))

    # 3 — top credit block in first 30 lines
    head = "\n".join(lines[:30])
    for m in TOP_CREDIT_RE.finditer(head):
        lineno = head[: m.start()].count("\n") + 1
        issues.append((tag, "TOP-CREDIT", f"Line ~{lineno}: credit block in first 30 lines — {m.group().strip()[:60]}"))

    # 4 — Markdown footnote syntax
    for i, line in enumerate(lines, 1):
        if MARKDOWN_FOOTNOTE_RE.search(line):
            issues.append((tag, "MD-FOOTNOTE", f"Line {i}: Markdown footnote [^ detected — {line[:80]}"))

    # 5 — bare URL followed by Japanese
    for i, line in enumerate(lines, 1):
        if BARE_URL_KANJI_RE.search(line):
            issues.append((tag, "BARE-URL", f"Line {i}: bare URL + Japanese — {line[:100]}"))

    # 6 — unlinked takasumasakazu.net
    for i, line in enumerate(lines, 1):
        if UNLINKED_CREDIT_URL_RE.search(line):
            issues.append((tag, "UNLINKED-URL", f"Line {i}: unlinked https://takasumasakazu.net — {line[:80]}"))

    # 7 — local translation-guide link
    for i, line in enumerate(lines, 1):
        if LOCAL_GUIDE_RE.search(line):
            issues.append((tag, "LOCAL-GUIDE", f"Line {i}: local 翻訳方鷗 link; should point to GitHub — {line[:80]}"))

    # 8 — discouraged terms
    for term, replacement in DISCOURAGED_TERMS:
        for i, line in enumerate(lines, 1):
            if term in line:
                issues.append((tag, "TERM", f"Line {i}: discouraged 「{term}」 (use 「{replacement}」) — {line[:80]}"))

    # 9 — collect referenced images
    referenced = set()
    for m in IMAGE_REF_RE.finditer(text):
        referenced.add(m.group(1))

    return referenced


def check_images(all_image_files, referenced_by_target):
    """Return list of unreferenced page-render images."""
    unreferenced = []
    for img in sorted(all_image_files):
        if img.name not in referenced_by_target:
            unreferenced.append(img.name)
    return unreferenced


def check_package_lock():
    """Warn if package-lock.json appears modified (newer than any .md)."""
    if not PACKAGE_LOCK.exists():
        return False
    # Simple existence check; in a real git repo we'd use `git status`.
    # Here we just note it exists for the operator.
    return True


def main():
    chapters = parse_args(sys.argv)
    chapter_files = find_chapter_files(chapters)

    if not chapter_files:
        print("No chapter files found.")
        sys.exit(1)

    all_image_files = list(IMAGES_DIR.glob("page-*-render.png")) if IMAGES_DIR.exists() else []

    issues = []
    all_referenced = set()

    print(f"Checking {len(chapter_files)} chapter(s)...\n")
    for num, path in chapter_files:
        referenced = check_chapter(num, path, all_image_files, issues)
        all_referenced.update(referenced)

    # Unreferenced images (only page renders not referenced by *target* chapters)
    unreferenced_imgs = check_images(all_image_files, all_referenced)

    # ── print report ──────────────────────────────────────────────────────────
    if issues:
        print("=" * 60)
        print("ISSUES FOUND")
        print("=" * 60)
        for tag, kind, msg in issues:
            print(f"  [{kind}] {tag}: {msg}")
        print()

    if unreferenced_imgs:
        print("UNREFERENCED page renders (not referenced by target chapter(s)):")
        for img in unreferenced_imgs:
            print(f"  {img}")
        print()

    if not issues and not unreferenced_imgs:
        print("✓ All checks passed.")
    else:
        total = len(issues)
        serious = [i for i in issues if i[1] not in ("TERM", "UNLINKED-URL", "LOCAL-GUIDE")]
        print(f"Total issues: {total}  ({len(serious)} serious)")

    sys.exit(1 if issues else 0)


if __name__ == "__main__":
    main()
