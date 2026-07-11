Translate one chapter or a range of chapters/appendices of *Hacking the Xbox* into Japanese.

**Chapters end at 13. Do not create ch14.md or ch15.md. Appendices use `appendix-a.md` through `appendix-f.md`.**

**Argument:** chapter number, range, appendix, or appendix range passed after the command name.
Examples: `13` | `10-13` | `appendix-a` | `appendix-a-f` | `13 appendix-a-f`

**Instructions:**
1. Read `.claude/skills/xbox-translate-batch/SKILL.md` for the full procedure.
2. Follow `CLAUDE.md`, `TRANSLATION_GUIDE.md`, and `glossary.tsv`.
3. Use the Standard chapter translation workflow in `CLAUDE.md`.
4. Use **English** for all reports, logs, TODOs, and commit messages.
5. Use **Japanese** only for translated reader-facing content in `docs/ja/`.
6. Never commit or push. Never create ch14.md or ch15.md.
7. Pass the target range to `scripts/check_translation_batch.py` after translating.
