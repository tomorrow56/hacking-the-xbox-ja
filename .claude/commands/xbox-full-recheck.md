Revalidate all existing translated Japanese chapters against the latest rules.

**Argument (optional):** `all`, a range `N-M`, or two numbers `N M`. Defaults to all chapters.
Examples: *(no argument)* | `all` | `1-15` | `10 15`

**Instructions:**
1. Read `.claude/skills/xbox-full-recheck/SKILL.md` for the full procedure.
2. Read the current `CLAUDE.md`, `TRANSLATION_GUIDE.md`, and `glossary.tsv` — ignore prior chat history.
3. Run `python3 scripts/check_translation_batch.py all` (or the requested range).
4. Run `python3 scripts/validate_links.py`.
5. Perform qualitative review of chapters against `TRANSLATION_GUIDE.md`.
6. **Review only.** Do **not** retranslate or edit `docs/ja/*.md` unless the user explicitly requests a separate fix task.
7. Report in **English**, grouped by chapter and severity.
