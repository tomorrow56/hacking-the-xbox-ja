Review already-translated chapters without retranslating or rewriting prose.

**Argument:** chapter number or range.
Examples: `13` | `13-15` | `10 12`

**Instructions:**
1. Read `.claude/skills/xbox-postcheck/SKILL.md` for the full procedure.
2. Run (or recommend) `python3 scripts/check_translation_batch.py N M`.
3. Run `python3 scripts/validate_links.py`.
4. Ask the user to run `npm run docs:build` on Windows if needed.
5. Do **not** edit chapters unless the user explicitly asks.
6. Report findings in **English**, grouped by severity (must fix / should fix / optional).
