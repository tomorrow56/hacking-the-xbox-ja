Translate one chapter or a range of *Hacking the Xbox* chapters into Japanese.

**Argument:** chapter number or range passed after the command name.
Examples: `13` | `13-15` | `13 15`

**Instructions:**
1. Read `.claude/skills/xbox-translate-batch/SKILL.md` for the full procedure.
2. Follow `CLAUDE.md`, `TRANSLATION_GUIDE.md`, and `glossary.tsv`.
3. Use the Standard chapter translation workflow in `CLAUDE.md`.
4. Use **English** for all reports, logs, TODOs, and commit messages.
5. Use **Japanese** only for translated reader-facing content in `docs/ja/`.
6. Never commit or push.
7. Pass the target chapter range to `scripts/check_translation_batch.py` after translating.
