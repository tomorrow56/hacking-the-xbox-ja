# Hacking the Xbox — 日本語訳

## 読む

日本語訳はこちらから読めます：

https://takasumasakazu.net/hacking-the-xbox-ja/

## この翻訳について

本リポジトリは、Andrew "bunnie" Huang 著 *Hacking the Xbox: An Introduction to Reverse Engineering* の日本語訳プロジェクトです。

原著は Creative Commons BY-NC-SA 1.0 ライセンスで公開されており、本翻訳もその条件に従って公開しています。出版社による公式日本語版ではありません。

## フィードバック歓迎

誤訳、技術的な不正確さ、日本語として読みにくい箇所、図版の抜けなどがあれば、Issueで知らせてください。

GitHub Pages の公開サイトを開けば、そのまま読めます。

---

## License

- **Book-derived text, images, and translations**: CC BY-NC-SA 1.0  
  Copyright © 2003 Xenatera LLC (Author: Andrew "bunnie" Huang, Publisher: No Starch Press)
- **Scripts and site config**: MIT License

See [CONTENT-LICENSE.md](CONTENT-LICENSE.md) for full details.

## Translation status

## Translation status

| Section | Status |
|---------|--------|
| Dear Reader | translated / review ongoing |
| Acknowledgments | translated / review ongoing |
| Prologue — README.1ST | translated / review ongoing |
| Chapter 1 — Voiding the Warranty | translated / review ongoing |
| Chapter 2 — Thinking Inside the Box | translated / review ongoing |
| Chapter 3 — Installing a Blue LED | translated / review ongoing |
| Chapter 4 | translated / review ongoing |
| Chapter 5 | translated / review ongoing |
| Chapter 6 | translated / review ongoing |
| Chapters 7–13 | not started |
| Appendices A–F | not started |

---

## Development / 翻訳・開発者向け

**All translation work must follow [`TRANSLATION_GUIDE.md`](TRANSLATION_GUIDE.md) and [`glossary.tsv`](glossary.tsv).**

- Before translating any chapter, read `TRANSLATION_GUIDE.md` in full.
- Before translating any technical term, check `glossary.tsv`. Add missing terms before translating.
- See `CLAUDE.md` for operational rules (AI assistant instructions).

### Local setup

```bash
# 1. Install dependencies
npm install

# 2. The PDF is already at source/HackingTheXbox_Free.pdf (DO NOT re-download)

# 3. Extract text and images from the PDF
pip install pdfplumber pypdfium2 pikepdf
python3 scripts/extract_text.py
python3 scripts/extract_images.py

# 4. Copy extracted images to VitePress public dir
cp source/extract/images/* docs/public/images/

# 5. Validate links
python3 scripts/validate_links.py

# 6. Dev server
npm run docs:dev

# 7. Build
npm run docs:build
```

### GitHub Pages deployment

A GitHub Actions workflow is at `.github/workflows/deploy.yml`. It runs automatically on every push to `main`.

To enable GitHub Pages: repo Settings → Pages → Source: GitHub Actions.


