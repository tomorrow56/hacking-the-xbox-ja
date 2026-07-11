# Skill: xbox-postcheck

Review already-translated chapters/appendices for rule violations. **Do not retranslate
or rewrite prose** unless the user explicitly requests a separate fix task.

## Invocation

```
/xbox-postcheck 13
/xbox-postcheck 10-13
/xbox-postcheck appendix-a
/xbox-postcheck appendix-a-f
/xbox-postcheck 13 appendix-a-f
/xbox-postcheck 10 12
```

## Procedure

1. Run the deterministic harness for the target range:
   ```bash
   python3 scripts/check_translation_batch.py 13
   python3 scripts/check_translation_batch.py appendix-a
   python3 scripts/check_translation_batch.py 13 appendix-a-f
   # or all:
   python3 scripts/check_translation_batch.py all
   ```

2. Run link validation:
   ```bash
   python3 scripts/validate_links.py
   ```

3. Ask the user to run on Windows if needed:
   ```powershell
   npm run docs:build
   ```

4. Summarize findings in English. Group by chapter/appendix. Flag severity:
   - **must fix**: figure labels, top credit blocks, mojibake, broken links
   - **should fix**: bare URLs, unlinked credits, discouraged terms
   - **optional**: style improvements

## Issues to flag

- Visible `Figure N-M` or `Figure A-1` in Japanese prose/captions (should be `図N-M` / `図A-1`)
- Top credit/license blockquotes within first 30 lines
- Unreferenced page renders in `docs/public/images/`
- Bare URLs followed directly by Japanese text
- Mojibake or replacement characters
- Markdown footnote syntax (`[^n]`)
- Build or link errors
- `package-lock.json` modifications
- Discouraged terms: サイドバー, アリゲータークリップ

## Hard constraints

- Read-only unless user explicitly asks to apply a fix.
- Never retranslate. Never create ch14.md or ch15.md.
- Never commit or push.
- Report in English.
