# Skill: xbox-translate-batch

Translate one chapter or a range of chapters/appendices of *Hacking the Xbox* into Japanese.

## Book structure

- Numbered chapters end at **Chapter 13**. Do not create ch14.md or ch15.md.
- After Chapter 13: **Appendix A–F**, stored as `docs/ja/appendix-a.md` through `docs/ja/appendix-f.md`.
- Do not refer to appendices as chapters.

## Invocation

```
/xbox-translate-batch 13
/xbox-translate-batch 10-13
/xbox-translate-batch appendix-a
/xbox-translate-batch appendix-a-f
/xbox-translate-batch 13 appendix-a-f
```

Parse the argument(s):
- Single digit / `N-M` / two digits → chapter(s), max 13
- `appendix-X` → single appendix (letter a–f)
- `appendix-X-Y` → appendix range X through Y

## Required reading (do this first, every time)

1. `CLAUDE.md` — operational rules, Standard chapter translation workflow, and book structure
2. `TRANSLATION_GUIDE.md` — style, figure rules, footnotes, callout format
3. `glossary.tsv` — term dictionary; check before every technical term
4. `source/chapter-map.json` — confirmed PDF page ranges (chapters and appendices)
5. `docs/.vitepress/config.mts` — existing sidebar entries

## Workflow — follow CLAUDE.md §Standard chapter translation workflow

**Step 1 — Verify repo state**
`git status && git log --oneline -3`. Confirm clean tree.

**Step 2 — Determine page range**
Read `source/chapter-map.json` for `pdf_pages_confirmed`. Scan boundary pages in
`source/extract/pages/` to confirm start/end. Record `pdf_page_range` and `printed_page_range`.

**Step 3 — Extract source text**
Check whether `source/extract/pages/page-NNN.txt` exists. If missing, extract with
pdfplumber (see CLAUDE.md §Step 4). **Translate only from extracted text.**

**Step 4 — Extract images (only pages with referenced figures)**
Use pypdfium2 at scale=2.0. Extract only pages that contain a figure the
chapter/appendix actually references. Skip blank pages and pages outside the range.

**Step 5 — Write the translation file**

| Target type | Output file | Title frontmatter |
|-------------|-------------|-------------------|
| Chapter N | `docs/ja/chNN.md` | `'第N章 タイトル'` |
| Appendix X | `docs/ja/appendix-x.md` | `'付録X タイトル'` |

Required frontmatter for both:
```yaml
pdf_page_range: 'START-END'
printed_page_range: 'START-END'
translation_status: draft
```

Key rules from TRANSLATION_GUIDE.md:
- **Figure labels**: chapters → `図N-M`; appendices → `図A-1`, `図B-2` etc. Never leave `Figure N-M` or `Figure A-1` visible in prose.
- **Callout boxes**: `> **📦 コラム：タイトル**` format; never use サイドバー.
- **Footnotes**: `<sup>N</sup>` inline + `## 注` section; no `[^n]` Markdown syntax.
- **URLs**: always `[url](url)` links; no bare URLs followed by Japanese text.
- **First-person**: 「僕」 for bunnie's narration.
- **No credit blockquote** under the chapter/appendix title.
- **Canonical `<small>` attribution footer** at the very bottom.
- **Write with `path.write_bytes(text.encode('utf-8'))`** — never the Edit tool.

**Step 6 — Update navigation**
- Chapters → add to 本文 sidebar group in `docs/.vitepress/config.mts`.
- Appendices → add to a 付録 sidebar group (create if it doesn't exist).
- Update `docs/index.md` with the new link.
- Write both files with `write_bytes(content.encode('utf-8'))`.

**Step 7 — Validate**
```bash
python3 scripts/check_translation_batch.py 13          # or: appendix-a
python3 scripts/validate_links.py
```
`npm run docs:build` cannot run in the Linux sandbox — ask user to run on Windows.

**Step 8 — Report (English only)**
Files changed + sizes, PDF range, images extracted, script output, deviations, TODOs, and:
```powershell
git add docs/ja/chNN.md docs/.vitepress/config.mts docs/index.md docs/public/images/ source/extract/pages/
git commit -m "trans: translate chapter N — Title (draft)"
# or for appendix:
git commit -m "trans: translate appendix X — Title (draft)"
```

## Hard constraints

- Chapters end at **13**. Never create ch14.md or ch15.md.
- Never commit or push.
- Never edit `package-lock.json`, `docs/credits.md`, or previously translated files.
- English for all reports, logs, TODOs, and commit messages.
- Japanese only for translated reader-facing content.
