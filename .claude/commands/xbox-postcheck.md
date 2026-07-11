Review already-translated chapters/appendices without retranslating or rewriting prose.

**Argument:** chapter number, range, appendix, or appendix range.
Examples: `13` | `10-13` | `appendix-a` | `appendix-a-f` | `13 appendix-a-f`

**Instructions:**
1. Read `.claude/skills/xbox-postcheck/SKILL.md` for the full procedure.
2. Run (or recommend) `python3 scripts/check_translation_batch.py <target>`.
3. Run `python3 scripts/validate_links.py`.
4. Ask the user to run `npm run docs:build` on Windows if needed.
5. Do **not** edit chapters or appendices unless the user explicitly asks.
6. Report findings in **English**, grouped by severity (must fix / should fix / optional).
