# Skill: xbox-postcheck

Review already-translated chapters for rule violations. **Do not retranslate or rewrite
chapter prose** unless the user explicitly requests a separate fix task.

## Invocation

```
/xbox-postcheck 13
/xbox-postcheck 13-15
/xbox-postcheck 10 12
```

Parse the argument(s): single number = one chapter; `N-M` or two numbers = inclusive range.

## Procedure

1. Run the deterministic harness:
   ```bash
   python3 scripts/check_translation_batch.py N M
   ```
   If checking all translated chapters:
   ```bash
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

4. Summarize findings in English. Group by chapter. Flag severity:
   - **must fix**: figure labels, top credit blocks, mojibake, broken links
   - **should fix**: bare URLs, unlinked credits, discouraged terms
   - **optional**: style improvements

## Issues to flag

- Visible `Figure N-M` labels in Japanese prose or captions (should be `図N-M`)
- Missing `図N-M` labels where figure references exist
- Top credit/license blockquotes within first 30 lines
- Unreferenced page renders in `docs/public/images/`
- `docs/public/images` files not referenced by any target chapter
- Bare URLs followed directly by Japanese text
- Mojibake or replacement characters (`�`)
- Markdown footnote syntax (`[^n]`)
- Build or link errors
- `package-lock.json` modifications
- Discouraged terms: `サイドバー`, `アリゲータークリップ`

## Hard constraints

- Read-only unless user explicitly asks to apply a fix.
- Never retranslate.
- Never commit or push.
- Report in English.
