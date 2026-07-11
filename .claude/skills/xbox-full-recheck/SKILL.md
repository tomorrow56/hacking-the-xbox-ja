# Skill: xbox-full-recheck

Revalidate all existing translated Japanese chapters and appendices against the latest
TRANSLATION_GUIDE.md and glossary.tsv.

**Review only. Do not retranslate or rewrite files unless the user explicitly
requests a separate fix task.**

## Invocation

```
/xbox-full-recheck
/xbox-full-recheck all
/xbox-full-recheck 1-13
/xbox-full-recheck 10-13
/xbox-full-recheck appendix-a-f
/xbox-full-recheck 10-13 appendix-a-f
```

With no argument or `all`, check every `docs/ja/chNN.md` and `docs/ja/appendix-X.md` that exists.

**The book has chapters 1–13 and appendices A–F. There is no Chapter 14 or 15.**

## Required reading (do this first)

1. `CLAUDE.md` — includes book structure note
2. `TRANSLATION_GUIDE.md` — treat the repo file as the authoritative source of rules
3. `glossary.tsv`

Ignore prior chat history. The repo files are the ground truth.

## Level 1 — Deterministic script checks

```bash
python3 scripts/check_translation_batch.py all
# or for a specific range:
python3 scripts/check_translation_batch.py 10 13
python3 scripts/check_translation_batch.py appendix-a-f
```

```bash
python3 scripts/validate_links.py
```

Ask the user to run on Windows:
```powershell
npm run docs:build
```

## Level 2 — Claude qualitative review

Review each target file against TRANSLATION_GUIDE.md. Check for:

**Figure / image issues**
- Visible `Figure N-M` or `Figure A-1` in prose or captions (must be `図N-M` / `図A-1`)
- Image/caption mismatches; duplicated same-page renders; unreferenced renders
- Accidental next-chapter or end-matter content

**Credits / footers**
- Top credit/license blockquote under title (must not exist)
- Canonical `<small>` attribution footer at bottom (must exist)
- `https://takasumasakazu.net` linked as Markdown link (not bare URL)
- Local 翻訳方針 page references instead of GitHub TRANSLATION_GUIDE.md link

**Terminology / glossary**
- Glossary violations; inconsistent electronics/security terminology
- Unexpanded abbreviations on first use; bit/byte mistakes (8Mbit ≠ 8MB)
- サイドバー → コラム / 囲み記事; アリゲータークリップ → ワニ口クリップ

**Prose / style**
- English-shaped Japanese; stiff machine-translation phrases
- Japanese operational text where English is required

**Markdown / links**
- Bare URLs followed by Japanese text
- Broken Markdown links; Markdown footnote syntax `[^...]`
- Mojibake or replacement characters

## Report format

- English only. Do not paste full chapter text.
- Group by file then by severity: **must fix** / **should fix** / **optional**.
- Include file path and a short excerpt. Representative examples for recurring patterns.
- If no major issues, say so clearly.

## Hard constraints

- Never edit `docs/ja/*.md` or images.
- Never retranslate. Never reference ch14 or ch15.
- Never commit or push.
- Report in English.
