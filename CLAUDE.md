# CLAUDE.md — Hacking the Xbox 非公式日本語訳

## Operational rules

1. **Always read `TRANSLATION_GUIDE.md` before any translation work.**
2. **Always consult `glossary.tsv` before translating technical terms.**
3. **Work and report in English** to reduce token usage. Japanese is required only for translated book content and public-facing Japanese pages (`docs/ja/`, `docs/index.md`). See **§ Operational language** below for the full rule.
4. **Never push** to any remote unless explicitly instructed by the user.
5. **Do not call a chapter complete** unless all of the following are done:
   - Source PDF text extracted and stored in `source/extract/pages/`
   - Translation written from the extracted source text (not from memory or assumptions)
   - Images extracted and referenced correctly in `docs/public/images/`
   - Figure captions translated and placed adjacent to the correct image
   - `python3 scripts/validate_links.py` passes with zero errors
   - Frontmatter fields `pdf_page_range`, `printed_page_range`, `translation_status` are accurate
6. **Do not re-state the full guide in reports.** Only report deviations from the guide, TODOs, errors, and quantitative results (page counts, image counts, validation output).
7. **The PDF is local only** at `source/HackingTheXbox_Free.pdf`. Never attempt to download it from the internet.
8. **Use pdfplumber for text extraction** and `pikepdf` or `pypdfium2` for image extraction (PyMuPDF/fitz is not installed in this environment).

## Operational language

Use **English** for all workflow and development operations. This reduces token usage and keeps operational output unambiguous.

**Always English:**
- Claude reports, progress summaries, and explanations of changed files
- Validation and build result summaries
- Suggested commit messages and actual git commit messages
- Branch names, PR titles, and PR descriptions
- TODO comments that are not reader-facing
- Internal notes about source page ranges, figures, validation, and build results

**Always Japanese:**
- Translated book content (`docs/ja/*.md`)
- Japanese reader-facing site text (homepage, credits, nav labels)
- Japanese captions and headings inside translated pages
- Japanese examples that intentionally belong in the translation

**Commit messages must be in English.**

Good:
```
trans: add Chapter 9 Japanese translation (draft)
fix: standardize Japanese figure labels
guide: update operational language rules
docs: update credit footer links
fix: repair VitePress config string literal
```

Bad (do not use Japanese in commit messages):
```
第8章の日本語訳を追加
図表記を修正
翻訳ルールを更新
```

Do not produce Japanese operational summaries unless the user explicitly asks for them.

## Standard chapter translation workflow

Use this sequence for every chapter. Vary only if the user specifies otherwise.

**Step 1 — Verify repo state**
```
cd D:\hackingthexbox && git status && git log --oneline -3
```
Confirm clean working tree and correct HEAD before touching any file.

**Step 2 — Read project files**
Read in this order (required before any translation):
1. `TRANSLATION_GUIDE.md` — rules, style, checklist
2. `glossary.tsv` — term dictionary
3. `source/chapter-map.json` — chapter/page mapping
4. `docs/.vitepress/config.mts` — sidebar (to see existing entries)

**Step 3 — Determine source page range**
- Check `source/chapter-map.json` for `pdf_pages_confirmed` for the chapter.
- Open `source/HackingTheXbox_Free.pdf` with pdfplumber; scan the first/last pages of the range to confirm chapter start/end boundaries.
- Record: `pdf_page_range` (e.g. `"119-135"`) and `printed_page_range` (printed numbers shown in book footer).

**Step 4 — Extract source text**
```python
import pdfplumber, pathlib
pdf = pdfplumber.open("source/HackingTheXbox_Free.pdf")
out = pathlib.Path("source/extract/pages")
out.mkdir(parents=True, exist_ok=True)
for pn in range(start, end+1):  # 1-based PDF page numbers
    text = pdf.pages[pn-1].extract_text() or ""
    (out / f"page-{pn:03d}.txt").write_text(text, encoding="utf-8")
```
Translate **only from extracted text**, never from memory.

**Step 5 — Extract images**
```python
import pypdfium2 as pdfium, pathlib
doc = pdfium.PdfDocument("source/HackingTheXbox_Free.pdf")
out = pathlib.Path("docs/public/images")
out.mkdir(parents=True, exist_ok=True)
for pn in range(start, end+1):  # 0-based for pypdfium2
    page = doc[pn-1]
    bm = page.render(scale=2.0)
    bm.to_pil().save(out / f"page-{pn:03d}-render.png")
```
Verify each PNG exists before referencing it in the chapter file.

**Step 6 — Translate**
Write `docs/ja/chNN.md` using:
- Frontmatter: `title`, `pdf_page_range`, `printed_page_range`, `translation_status: draft`
- Chapter content translated per `TRANSLATION_GUIDE.md`
- Figures: use `page-NNN-render.png`; multi-caption rule when 2+ figures share a page
- Footnotes: inline `<sup>N</sup>` + `## 注` section; no Markdown footnote syntax
- Canonical `<small>` attribution footer at the bottom
- **No credit/license blockquote under the chapter title**
- Always write Japanese files with `path.write_bytes(text.encode('utf-8'))` — never the Edit tool

**Step 7 — Update navigation**
- `docs/.vitepress/config.mts`: add sidebar entry `{ text: '第N章 タイトル', link: '/ja/chNN' }`
- `docs/index.md`: add chapter link to the chapter list
- Write both with `write_bytes(content.encode('utf-8'))` after verifying full file length post-write

**Step 8 — Validate**
```
cd D:\hackingthexbox && python3 scripts/validate_links.py
```
Zero errors required before m

## Project skills (Claude Code slash commands)

Use these skills instead of writing long prompts from scratch.

| Skill | Purpose |
|-------|---------|
| `/xbox-translate-batch N` | Translate chapter N (or range N-M) end-to-end |
| `/xbox-postcheck N` | Review recent chapter(s) without retranslating |
| `/xbox-full-recheck` | Revalidate all translated chapters against latest rules |
| `/xbox-rule-update <description>` | Update TRANSLATION_GUIDE.md / glossary.tsv only |

Skills live in `.claude/skills/`. Each SKILL.md contains the full procedure.

**`/xbox-full-recheck` is review-only.** It must not retranslate or rewrite chapter
prose unless the user explicitly requests a separate fix task.

### Validation harness

```bash
python3 scripts/check_translation_batch.py all        # all chapters
python3 scripts/check_translation_batch.py 10 15      # range
python3 scripts/validate_links.py
```

`npm run docs:build` must be run on Windows (cannot run in Linux sandbox).

## Potential future hooks

- **PreToolUse hook**: block `git push` from Claude.
- **Stop hook**: suggest running `/xbox-postcheck` or `/xbox-full-recheck` after a
  translation session completes.
