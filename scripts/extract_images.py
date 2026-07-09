#!/usr/bin/env python3
"""
extract_images.py
Extract embedded images from source/HackingTheXbox_Free.pdf.
Output:
  source/extract/images/page-PPP-img-NNN.EXT
  source/extract/figures-manifest.json

The manifest lists every image with its page, bounding box, and xref.
Captions are heuristically detected from text on the same page.

Requires: PyMuPDF  ->  pip install pymupdf
Usage:    python3 scripts/extract_images.py [--pdf PATH] [--out DIR]
"""

import argparse
import json
import re
import sys
from pathlib import Path

try:
    import fitz  # PyMuPDF
except ImportError:
    print("ERROR: PyMuPDF is not installed. Run: pip install pymupdf", file=sys.stderr)
    sys.exit(1)

REPO_ROOT = Path(__file__).parent.parent
DEFAULT_PDF = REPO_ROOT / "source" / "HackingTheXbox_Free.pdf"
DEFAULT_IMAGES = REPO_ROOT / "source" / "extract" / "images"
MANIFEST_PATH = REPO_ROOT / "source" / "extract" / "figures-manifest.json"

# Pattern to detect figure captions like "Figure 1-1", "Figure 3-2", etc.
CAPTION_RE = re.compile(r"(Figure\s+\d+[\-\.]\d+[^\n]*)", re.IGNORECASE)


def extract_caption(page_text: str) -> list[str]:
    """Return all figure caption strings found on this page."""
    return CAPTION_RE.findall(page_text)


def extract(pdf_path: Path, images_dir: Path, manifest_path: Path) -> dict:
    images_dir.mkdir(parents=True, exist_ok=True)

    doc = fitz.open(str(pdf_path))
    manifest = []
    stats = {
        "total_pages": len(doc),
        "images_extracted": 0,
        "pages_with_images": 0,
        "errors": [],
    }

    print(f"PDF: {pdf_path.name}  ({len(doc)} pages)")

    for page_idx, page in enumerate(doc):
        page_num = page_idx + 1
        page_text = page.get_text("text")
        captions = extract_caption(page_text)
        image_list = page.get_images(full=True)

        if not image_list:
            continue

        stats["pages_with_images"] += 1

        for img_idx, img in enumerate(image_list):
            xref = img[0]
            try:
                base_image = doc.extract_image(xref)
                ext = base_image["ext"]  # e.g. "png", "jpeg"
                img_bytes = base_image["image"]

                filename = f"page-{page_num:03d}-img-{img_idx + 1:02d}.{ext}"
                out_path = images_dir / filename
                out_path.write_bytes(img_bytes)

                # Get bounding rectangle via page's image list metadata
                # (width/height available in base_image)
                entry = {
                    "filename": filename,
                    "page": page_num,
                    "img_index": img_idx + 1,
                    "xref": xref,
                    "width": base_image.get("width"),
                    "height": base_image.get("height"),
                    "colorspace": base_image.get("colorspace"),
                    "ext": ext,
                    "captions_on_page": captions,
                    "docs_path": f"/images/{filename}",
                }
                manifest.append(entry)
                stats["images_extracted"] += 1

            except Exception as e:
                err = {"page": page_num, "img_index": img_idx, "error": str(e)}
                stats["errors"].append(err)
                print(f"  WARN: page {page_num} img {img_idx}: {e}", file=sys.stderr)

        if page_num % 50 == 0 or page_num == len(doc):
            print(f"  {page_num}/{len(doc)} pages scanned ...", flush=True)

    doc.close()

    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(
        json.dumps({"stats": stats, "images": manifest}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print(
        f"\nDone. {stats['images_extracted']} images extracted from "
        f"{stats['pages_with_images']} pages."
    )
    print(f"Manifest: {manifest_path}")
    return stats


def main():
    ap = argparse.ArgumentParser(description="Extract images from Hacking the Xbox PDF")
    ap.add_argument("--pdf", type=Path, default=DEFAULT_PDF)
    ap.add_argument("--out", type=Path, default=DEFAULT_IMAGES)
    ap.add_argument("--manifest", type=Path, default=MANIFEST_PATH)
    args = ap.parse_args()

    if not args.pdf.exists():
        print(f"ERROR: PDF not found at {args.pdf}", file=sys.stderr)
        print("Place the PDF at source/HackingTheXbox_Free.pdf and retry.", file=sys.stderr)
        sys.exit(1)

    extract(args.pdf, args.out, args.manifest)


if __name__ == "__main__":
    main()
