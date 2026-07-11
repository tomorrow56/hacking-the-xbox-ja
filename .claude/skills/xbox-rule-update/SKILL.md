# Skill: xbox-rule-update

Update translation rules without touching translated content.

## Invocation

```
/xbox-rule-update figure labels must be 図N-M
/xbox-rule-update do not use Japanese commit messages
/xbox-rule-update credit footer URL must be a Markdown link
```

The argument is a free-form description of the rule change.

## Allowed edits

| File | Purpose |
|------|---------|
| `TRANSLATION_GUIDE.md` | Prose/style/process rules |
| `glossary.tsv` | Stable term mappings |

**Never edit:**
- `docs/ja/*.md` (translated chapters)
- `CLAUDE.md` (operational rules — only if user explicitly names it)
- Any other file unless the user explicitly instructs

## Decision rule

- Stable, dictionary-style term mappings — add to `glossary.tsv`.
- Style, process, and prose rules — add/update in `TRANSLATION_GUIDE.md`.
- Keep rules compact. Do not duplicate content already present.

## After editing

Report in English:
- Which file(s) changed
- What was added/changed/removed (brief diff description)
- Whether any chapters need a retroactive fix (flag only; do not edit chapters)

PowerShell commit command:
```powershell
git add TRANSLATION_GUIDE.md glossary.tsv
git commit -m "guide: <brief description of rule change>"
```

## Hard constraints

- Never retranslate.
- Never commit or push.
- Never edit `package-lock.json`.
- Report in English.
