#!/usr/bin/env python3
"""
extract_text.py
Extract plain text from source/HackingTheXbox_Free.pdf page by page.
Output: source/extract/pages/page-XXX.txt (one file per PDF page)

Requires: pdfplumber  ->  pip install pdfplumber
Usage:    python3 scripts/extract_text.py [PDF_PATH]
"""
import argparse
import json
import sys
from pathlib import Path

try:
    import pdfplumber
except ImportError:
    print("ERROR: pdfplumber not installed. Run: pip install pdfplumber", file=sys.stderr)
    sys.exit(1)

REPO_ROOT = Path(__file__).parent.parent
DEFAULT_PDF = REPO_ROOT / "source" / "HackingTheXbox_Free.pdf"
DEFAULT_OUT = REPO_ROOT / "source" / "extract" / "pages"


def extract(pdf_path: Path, out_dir: Path) -> dict:
    out_dir.mkdir(parents=True, exist_ok=True)
    stats = {"total_pages": 0, "extracted": 0, "empty": 0, "errors": []}

    with pdfplumber.open(str(pdf_path)) as pdf:
        total = len(pdf.pages)
        stats["total_pages"] = total
        print(f"PDF: {pdf_path.name}  ({total} pages)")

        for i, page in enumerate(pdf.pages):
            page_num = i + 1
            out_file = out_dir / f"page-{page_num:03d}.txt"
            try:
                text = page.extract_text() or ""
                out_file.write_text(text, encoding="utf-8")
                if text.strip():
                    stats["extracted"] += 1
                else:
                    stats["empty"] += 1
            except Exception as e:
                stats["errors"].append({"page": page_num, "error": str(e)})
                out_file.write_text(f"<!-- EXTRACT_ERROR: {e} -->", encoding="utf-8")
                print(f"  WARN page {page_num}: {e}", file=sys.stderr)

            if page_num % 50 == 0 or page_num == total:
                print(f"  {page_num}/{total}", flush=True)

    summary_path = out_dir.parent / "text-extract-summary.json"
    summary_path.write_text(
        json.dumps(stats, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(f"\nDone. extracted={stats['extracted']} empty={stats['empty']} errors={len(stats['errors'])}")
    print(f"Summary: {summary_path}")
    return stats


def main():
    ap = argparse.ArgumentParser(description="Extract text from Hacking the Xbox PDF")
    ap.add_argument("pdf", nargs="?", type=Path, default=DEFAULT_PDF, help="Source PDF path")
    ap.add_argument("--out", type=Path, default=DEFAULT_OUT, help="Output directory")
    args = ap.parse_args()

    if not args.pdf.exists():
        print(f"ERROR: PDF not found at {args.pdf}", file=sys.stderr)
        sys.exit(1)

    extract(args.pdf, args.out)


if __name__ == "__main__":
    main()
