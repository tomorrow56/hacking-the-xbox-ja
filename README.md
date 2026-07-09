# Hacking the Xbox — 非公式日本語訳

非公式日本語翻訳サイト for *Hacking the Xbox: An Introduction to Reverse Engineering*  
by Andrew "bunnie" Huang | Copyright © 2003 Xenatera LLC | Published by No Starch Press

**This is an UNOFFICIAL, NONCOMMERCIAL fan translation (非公式日本語訳).**  
**Not endorsed by the author, Xenatera LLC, or No Starch Press.**

---

> **TODO (deployment):** The VitePress `base` in `docs/.vitepress/config.ts` is currently set to
> `"/hacking-the-xbox-ja/"`. If the final GitHub repository name differs, update `base` in
> `docs/.vitepress/config.ts` to match the actual repository name before deploying.

---

## Setup

```bash
# 1. Install dependencies
npm install

# 2. Get the free PDF (released by No Starch Press under CC BY-NC-SA 1.0)
#    https://nostarch.com/xboxfree
mkdir -p source
# Place the PDF at: source/HackingTheXbox_Free.pdf

# 3. Extract text and images from the PDF (requires PyMuPDF)
pip install pymupdf
python3 scripts/extract_text.py
python3 scripts/extract_images.py

# 4. Copy extracted images to VitePress public dir
cp source/extract/images/* docs/public/images/

# 5. Dev server
npm run docs:dev

# 6. Build
npm run docs:build
```

## GitHub Pages Deployment

A GitHub Actions workflow is included at `.github/workflows/deploy.yml`.

**Prerequisites before deployment:**
1. Create the GitHub repository (name: `hacking-the-xbox-ja` or update `base` in config)
2. Enable GitHub Pages in repo Settings → Pages → Source: GitHub Actions
3. Push to `main` branch — the workflow will build and deploy automatically

No remote origin is configured yet. This is a local-only repository.

## License

- **Book-derived text, images, and translations**: CC BY-NC-SA 1.0  
  Copyright © 2003 Xenatera LLC (Author: Andrew "bunnie" Huang, Publisher: No Starch Press)
- **Scripts and site config**: MIT License

See [CONTENT-LICENSE.md](CONTENT-LICENSE.md) for full details.

## Translation Status

| Section | Status |
|---------|--------|
| Prologue | draft |
| Chapter 1 | draft |
| Chapters 2–13 | not started |
| Appendices A–F | not started |
