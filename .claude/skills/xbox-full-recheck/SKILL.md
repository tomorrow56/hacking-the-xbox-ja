# Skill: xbox-full-recheck

Revalidate all existing translated Japanese chapters against the latest
TRANSLATION_GUIDE.md and glossary.tsv.

**Review only. Do not retranslate or rewrite chapters unless the user explicitly
requests a separate fix task.**

## Invocation

```
/xbox-full-recheck
/xbox-full-recheck all
/xbox-full-recheck 1-15
/xbox-full-recheck 10-15
```

With no argument or `all`, check every `docs/ja/chNN.md` that exists.

## Required reading (do this first)

1. `CLAUDE.md`
2. `TRANSLATION_GUIDE.md` — treat the repo file as the authoritative source of rules
3. `glossary.tsv`

Ignore prior chat history. The repo files are the ground truth.

## Level 1 — Deterministic script checks

```bash
python3 scripts/check_translation_batch.py all
# or for a range:
python3 scripts/check_translation_batch.py 10 15
```

```bash
python3 scripts/validate_links.py
```

Ask the user to run on Windows:
```powershell
npm run docs:build
```

## Level 2 — Claude qualitative review

Review each target chapter against TRANSLATION_GUIDE.md. Check for:

**Figure / image issues**
- Visible `Figure N-M` in prose or captions (must be `図N-M`)
- Image/caption mismatch risks
- Duplicated same-page full-page renders
- Unreferenced page renders
- Accidental next-chapter or end-matter content

**Credits / footers**
- Old top credit/license blockquote under chapter title
- Duplicate or stale footer wording
- Unlinked `https://takasumasakazu.net` in page-bottom credits
- Local `翻訳方針` page references instead of GitHub TRANSLATION_GUIDE.md link

**Terminology / glossary**
- Glossary violations (check glossary.tsv)
- Inconsistent electronics/security terminology
- Unexpanded abbreviations on first use (e.g. FPGA, ESD, LPC)
- Bit/byte mistakes (e.g. 8Mbit treated as 8MB)
- `サイドバー` where `コラム` / `囲み記事` is required
- `アリゲータークリップ` where `ワニ口クリップ` is required

**Prose / style**
- English-shaped Japanese phrasing
- Repeated awkward demonstratives (`この` / `その` / `こうした`)
- Stiff machine-translation phrases explicitly discouraged by TRANSLATION_GUIDE.md
- Japanese operational text where English is required (reports, TODOs)

**Markdown / links**
- Bare URLs followed directly by Japanese text
- Broken Markdown links
- Markdown footnote syntax `[^…]`
- Mojibake or replacement characters (`�`)

## Report format

- English only.
- Do not paste full chapter text.
- Group issues by chapter then by severity:
  - **must fix**
  - **should fix**
  - **optional style improvement**
- Include file path and a short excerpt to locate each issue.
- If a pattern recurs many times, give 2–3 representative examples and recommend a focused fix task.
- If no major issues are found, say so clearly.

## Hard constraints

- Never edit `docs/ja/*.md`.
- Never edit images.
- Never retranslate.
- Never commit or push.
- Report in English.
