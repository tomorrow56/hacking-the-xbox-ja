# Skill: xbox-translate-batch

Translate one chapter or a range of chapters of *Hacking the Xbox* into Japanese.

## Invocation

```
/xbox-translate-batch 13
/xbox-translate-batch 13-15
/xbox-translate-batch 13 15
```

Parse the argument(s): single number = one chapter; `N-M` or two numbers = inclusive range.

## Required reading (do this first, every time)

1. `CLAUDE.md` — operational rules and Standard chapter translation workflow
2. `TRANSLATION_GUIDE.md` — style, figure rules, footnotes, callout format
3. `glossary.tsv` — term dictionary; check before every technical term
4. `source/chapter-map.json` — confirmed PDF page ranges
5. `docs/.vitepress/config.mts` — existing sidebar entries

## Workflow — follow CLAUDE.md §Standard chapter translation workflow

**Step 1 — Verify repo state**
`git status && git log --oneline -3`. Confirm clean tree.

**Step 2 — Determine page range**
Read `source/chapter-map.json` for `pdf_pages_confirmed`. Scan boundary pages in
`source/extract/pages/` to confirm chapter start/end. Record `pdf_page_range` and
`printed_page_range`.

**Step 3 — Extract source text**
For each page, check whether `source/extract/pages/page-NNN.txt` exists. If missing,
extract with pdfplumber (see CLAUDE.md §Step 4). Translate **only from extracted
text — never from memory**.

**Step 4 — Extract images (only pages with referenced figures)**
Use pypdfium2 at scale=2.0. Do not extract blank pages or pages outside the chapter
range. See CLAUDE.md §Step 5.

**Step 5 — Write `docs/ja/chNN.md`**

Required frontmatter:
```yaml
title: '第N章 タイトル'
pdf_page_range: 'START-END'
printed_page_range: 'START-END'
translation_status: draft
```

Key rules from TRANSLATION_GUIDE.md:
- **Figure labels**: visible prose/captions → `図N-M`. Alt text and filenames may keep `Figure N-M`.
- **Callout boxes**: `> **📦 コラム：タイトル**` format; never use サイドバー.
- **Footnotes**: `<sup>N</sup>` inline + `## 注` section; no `[^n]` Markdown syntax.
- **URLs**: always `[url](url)` links; no bare URLs followed by Japanese text.
- **First-person**: 「僕」 for bunnie's narration.
- **No credit blockquote** under the chapter title.
- **Canonical `<small>` attribution footer** at the very bottom.
- **Write with `path.write_bytes(text.encode('utf-8'))`** — never the Edit tool.

**Step 6 — Update navigation**
- `docs/.vitepress/config.mts`: add sidebar entry.
- `docs/index.md`: add chapter link under `## 読む`.
- Write both with `write_bytes(content.encode('utf-8'))`.

**Step 7 — Validate**
```bash
python3 scripts/check_translation_batch.py N M
python3 scripts/validate_links.py
```
Both must pass. `npm run docs:build` cannot run in the Linux sandbox — ask user to run on Windows.

**Step 8 — Report (English only)**
Include: files changed + sizes, PDF range, images extracted, script output, deviations,
TODOs, and PowerShell commit command:
```powershell
git add docs/ja/chNN.md docs/.vitepress/config.mts docs/index.md docs/public/images/ source/extract/pages/
git commit -m "trans: translate chapter N — Title (draft)"
```

## Hard constraints

- Never commit or push.
- Never edit `package-lock.json`, `docs/credits.md`, or previously translated chapters.
- English for all reports, logs, TODOs, and commit messages.
- Japanese only for translated reader-facing content.
