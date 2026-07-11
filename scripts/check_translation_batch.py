#!/usr/bin/env python3
"""
check_translation_batch.py — read-only validation harness for Hacking the Xbox
Japanese translation chapters and appendices.

Usage:
    python3 scripts/check_translation_batch.py 13
    python3 scripts/check_translation_batch.py 10 13
    python3 scripts/check_translation_batch.py 10-13
    python3 scripts/check_translation_batch.py appendix-a
    python3 scripts/check_translation_batch.py appendix-a-f
    python3 scripts/check_translation_batch.py 13 appendix-a-f
    python3 scripts/check_translation_batch.py all

Book structure:
    Chapters 1–13  →  docs/ja/ch01.md … ch13.md
    Appendix A–F   →  docs/ja/appendix-a.md … appendix-f.md
"""

import re
import sys
import pathlib
from dataclasses import dataclass
from typing import List, Optional, Tuple, Set

# ── repo layout ──────────────────────────────────────────────────────────────
REPO = pathlib.Path(__file__).resolve().parent.parent
DOCS_JA = REPO / "docs" / "ja"
IMAGES_DIR = REPO / "docs" / "public" / "images"

MAX_CHAPTER = 13
APPENDIX_LETTERS = list("abcdef")

# ── target representation ────────────────────────────────────────────────────
@dataclass
class Target:
    kind: str        # 'chapter' or 'appendix'
    ident: object    # int for chapter, str letter for appendix

    @property
    def tag(self):
        if self.kind == 'chapter':
            return f"ch{self.ident:02d}"
        return f"appendix-{self.ident}"

    @property
    def path(self):
        if self.kind == 'chapter':
            return DOCS_JA / f"ch{self.ident:02d}.md"
        return DOCS_JA / f"appendix-{self.ident}.md"


def _chapter_targets(a: int, b: int) -> List[Target]:
    a = max(1, a); b = min(MAX_CHAPTER, b)
    return [Target('chapter', n) for n in range(a, b + 1)]


def _appendix_targets(a: str, b: str) -> List[Target]:
    lo = APPENDIX_LETTERS.index(a.lower())
    hi = APPENDIX_LETTERS.index(b.lower())
    return [Target('appendix', APPENDIX_LETTERS[i]) for i in range(lo, hi + 1)]


def parse_args(argv: List[str]) -> List[Target]:
    args = argv[1:]
    if not args or args == ["all"]:
        # all existing chapters + all existing appendices
        chapters = _chapter_targets(1, MAX_CHAPTER)
        appendices = _appendix_targets('a', 'f')
        return chapters + appendices

    targets: List[Target] = []
    i = 0
    while i < len(args):
        tok = args[i]
        # appendix-a or appendix-a-f
        m = re.fullmatch(r'appendix-([a-f])(?:-([a-f]))?', tok, re.IGNORECASE)
        if m:
            lo, hi = m.group(1).lower(), (m.group(2) or m.group(1)).lower()
            targets.extend(_appendix_targets(lo, hi))
            i += 1
            continue
        # pure digit: chapter N
        if re.fullmatch(r'\d+', tok):
            n = int(tok)
            # peek ahead: could be "N M" (chapter range)
            if i + 1 < len(args) and re.fullmatch(r'\d+', args[i + 1]):
                m2 = int(args[i + 1])
                targets.extend(_chapter_targets(n, m2))
                i += 2
                continue
            targets.extend(_chapter_targets(n, n))
            i += 1
            continue
        # N-M range
        m = re.fullmatch(r'(\d+)-(\d+)', tok)
        if m:
            targets.extend(_chapter_targets(int(m.group(1)), int(m.group(2))))
            i += 1
            continue
        print(f"WARNING: unrecognised argument {tok!r} — skipped", file=sys.stderr)
        i += 1

    if not targets:
        sys.exit(
            f"Usage: {argv[0]} N | N M | N-M | appendix-a | appendix-a-f | "
            "13 appendix-a-f | all"
        )
    return targets


def all_existing_targets() -> List[Target]:
    """Return targets for every file that actually exists."""
    found = []
    for p in sorted(DOCS_JA.glob("ch*.md")):
        mm = re.match(r"ch(\d+)\.md$", p.name)
        if mm:
            found.append(Target('chapter', int(mm.group(1))))
    for letter in APPENDIX_LETTERS:
        p = DOCS_JA / f"appendix-{letter}.md"
        if p.exists():
            found.append(Target('appendix', letter))
    return found


# ── check patterns ────────────────────────────────────────────────────────────
MOJIBAKE_RE = re.compile(r"�|\\ufffd")

# Figure N-M in prose (chapters): strip image markdown first
FIGURE_PROSE_CH_RE = re.compile(r"\bFigure\s+\d+[-–]\d+", re.IGNORECASE)
# Figure A-1 in prose (appendices)
FIGURE_PROSE_APP_RE = re.compile(r"\bFigure\s+[A-Fa-f][-–]\d+", re.IGNORECASE)

BARE_URL_JP_RE = re.compile(
    r"https?://[^\s\)\]>\"\']+[　-鿿＀-￯]"
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
    ("アリゲータークリップ",
     "ワニ口クリップ"),
]
TOP_CREDIT_RE = re.compile(
    r"^\s*\*?(?:原著|著者|著作権|出版"
    r"|本翻訳|日本語訳・レビュー)[:::]",
    re.MULTILINE,
)
IMAGE_REF_RE = re.compile(r"!\[.*?\]\(.*?/images/(page-\d{3}-render\.png)\)")


def check_target(t: Target, all_image_files: List[pathlib.Path],
                 issues: List[Tuple]) -> Set[str]:
    tag = t.tag
    path = t.path

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
            issues.append((tag, "MOJIBAKE",
                           f"Line {i}: replacement char detected — {line[:80]}"))

    # 2 — Figure N-M / Figure A-1 in visible prose (strip img markdown first)
    stripped = re.sub(r"!\[.*?\]\([^)]*\)", "", text)
    figure_re = FIGURE_PROSE_APP_RE if t.kind == 'appendix' else FIGURE_PROSE_CH_RE
    for mm in figure_re.finditer(stripped):
        lineno = text[:mm.start()].count("\n") + 1
        issues.append((tag, "FIGURE-LABEL",
                       f"Line ~{lineno}: visible English figure label — {mm.group()!r}"))

    # 3 — top credit block in first 30 lines
    head = "\n".join(lines[:30])
    for mm in TOP_CREDIT_RE.finditer(head):
        lineno = head[:mm.start()].count("\n") + 1
        issues.append((tag, "TOP-CREDIT",
                       f"Line ~{lineno}: credit block in first 30 lines — "
                       f"{mm.group().strip()[:60]}"))

    # 4 — Markdown footnote syntax
    for i, line in enumerate(lines, 1):
        if MARKDOWN_FOOTNOTE_RE.search(line):
            issues.append((tag, "MD-FOOTNOTE",
                           f"Line {i}: Markdown footnote [^ — {line[:80]}"))

    # 5 — bare URL followed by Japanese
    for i, line in enumerate(lines, 1):
        if BARE_URL_JP_RE.search(line):
            issues.append((tag, "BARE-URL",
                           f"Line {i}: bare URL + Japanese — {line[:100]}"))

    # 6 — unlinked takasumasakazu.net
    for i, line in enumerate(lines, 1):
        if UNLINKED_CREDIT_URL_RE.search(line):
            issues.append((tag, "UNLINKED-URL",
                           f"Line {i}: unlinked https://takasumasakazu.net — {line[:80]}"))

    # 7 — local translation-guide link
    for i, line in enumerate(lines, 1):
        if LOCAL_GUIDE_RE.search(line):
            issues.append((tag, "LOCAL-GUIDE",
                           f"Line {i}: local guide link; should point to GitHub — {line[:80]}"))

    # 8 — discouraged terms
    for term, replacement in DISCOURAGED_TERMS:
        for i, line in enumerate(lines, 1):
            if term in line:
                issues.append((tag, "TERM",
                               f"Line {i}: discouraged {term!r} (use {replacement!r}) — "
                               f"{line[:80]}"))

    # 9 — collect referenced images
    referenced: Set[str] = set()
    for mm in IMAGE_REF_RE.finditer(text):
        referenced.add(mm.group(1))

    return referenced


def main():
    argv = sys.argv
    # If "all" or no args, enumerate existing files; otherwise parse explicit list
    if len(argv) < 2 or argv[1:] == ["all"]:
        targets = all_existing_targets()
    else:
        targets = parse_args(argv)

    if not targets:
        print("No targets to check.")
        sys.exit(0)

    all_image_files = (list(IMAGES_DIR.glob("page-*-render.png"))
                       if IMAGES_DIR.exists() else [])

    issues: List[Tuple] = []
    all_referenced: Set[str] = set()

    ch_count = sum(1 for t in targets if t.kind == 'chapter')
    app_count = sum(1 for t in targets if t.kind == 'appendix')
    desc = []
    if ch_count:
        desc.append(f"{ch_count} chapter(s)")
    if app_count:
        desc.append(f"{app_count} appendix/appendices")
    print(f"Checking {', '.join(desc)}...\n")

    for t in targets:
        referenced = check_target(t, all_image_files, issues)
        all_referenced.update(referenced)

    # Unreferenced images
    unreferenced_imgs = [
        img.name for img in sorted(all_image_files)
        if img.name not in all_referenced
    ]

    # ── report ────────────────────────────────────────────────────────────────
    if issues:
        print("=" * 60)
        print("ISSUES FOUND")
        print("=" * 60)
        for tag, kind, msg in issues:
            print(f"  [{kind}] {tag}: {msg}")
        print()

    if unreferenced_imgs:
        print("UNREFERENCED page renders (not referenced by target file(s)):")
        for img in unreferenced_imgs:
            print(f"  {img}")
        print()

    if not issues and not unreferenced_imgs:
        print("✓ All checks passed.")
    else:
        total = len(issues)
        serious = [i for i in issues
                   if i[1] not in ("TERM", "UNLINKED-URL", "LOCAL-GUIDE")]
        print(f"Total issues: {total}  ({len(serious)} serious)")

    sys.exit(1 if issues else 0)


if __name__ == "__main__":
    main()
