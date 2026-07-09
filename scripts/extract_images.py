#!/usr/bin/env python3
"""
extract_images.py
Extract embedded images from source/HackingTheXbox_Free.pdf.
Output:
  source/extract/images/page-PPP-img-NNN.EXT
  source/extract/figures-manifest.json

Requires: pikepdf  ->  pip install pikepdf
Usage:    python3 scripts/extract_images.py [PDF_PATH]
"""
import argparse
import json
import re
import sys
from pathlib import Path

try:
    import pikepdf
    from pikepdf import PdfImage, PdfError
except ImportError:
    print("ERROR: pikepdf not installed. Run: pip install pikepdf", file=sys.stderr)
    sys.exit(1)

try:
    import pdfplumber
except ImportError:
    pdfplumber = None

REPO_ROOT = Path(__file__).parent.parent
DEFAULT_PDF = REPO_ROOT / "source" / "HackingTheXbox_Free.pdf"
DEFAULT_IMAGES = REPO_ROOT / "source" / "extract" / "images"
MANIFEST_PATH = REPO_ROOT / "source" / "extract" / "figures-manifest.json"

CAPTION_RE = re.compile(r"(Figure\s+\d+[\-\.]\d+[^\n]*)", re.IGNORECASE)


def get_page_captions(pdf_path: Path) -> dict[int, list[str]]:
    """Use pdfplumber to extract figure captions per page (1-indexed)."""
    captions: dict[int, list[str]] = {}
    if pdfplumber is None:
        return captions
    with pdfplumber.open(str(pdf_path)) as pdf:
        for i, page in enumerate(pdf.pages):
            text = page.extract_text() or ""
            found = CAPTION_RE.findall(text)
            if found:
                captions[i + 1] = found
    return captions


def extract(pdf_path: Path, images_dir: Path, manifest_path: Path) -> dict:
    images_dir.mkdir(parents=True, exist_ok=True)
    manifest: list[dict] = []
    stats = {
        "total_pages": 0,
        "images_extracted": 0,
        "pages_with_images": 0,
        "errors": [],
    }

    print(f"Extracting captions with pdfplumber...")
    captions_by_page = get_page_captions(pdf_path)

    print(f"Extracting images with pikepdf from {pdf_path.name}...")
    with pikepdf.open(str(pdf_path)) as pdf:
        stats["total_pages"] = len(pdf.pages)
        print(f"  PDF has {stats['total_pages']} pages")

        for page_idx, page in enumerate(pdf.pages):
            page_num = page_idx + 1
            resources = page.get("/Resources")
            if resources is None:
                continue
            xobjects = resources.get("/XObject")
            if xobjects is None:
                continue

            page_image_count = 0
            for name, xobj in xobjects.items():
                try:
                    xobj_obj = xobj.obj if hasattr(xobj, 'obj') else xobj
                    subtype = xobj_obj.get("/Subtype")
                    if str(subtype) != "/Image":
                        continue

                    img_idx = page_image_count + 1
                    pdfimage = PdfImage(xobj_obj)
                    # Determine extension
                    ext_map = {
                        "JPEG": "jpg", "JPEG2000": "jp2",
                        "PNG": "png", "CCITTFax": "tif",
                        "LZW": "png", "FlateDecode": "png",
                        "RunLengthDecode": "png",
                    }
                    filters = pdfimage.filters
                    ext = "png"
                    for f in filters:
                        f_clean = f.replace("/", "")
                        if f_clean in ext_map:
                            ext = ext_map[f_clean]
                            break

                    filename = f"page-{page_num:03d}-img-{img_idx:02d}.{ext}"
                    out_path = images_dir / filename

                    pdfimage.extract_to(fileprefix=str(out_path.with_suffix("")))
                    # pikepdf adds extension automatically; find the actual file
                    candidates = list(images_dir.glob(f"page-{page_num:03d}-img-{img_idx:02d}.*"))
                    actual_file = candidates[0] if candidates else out_path

                    entry = {
                        "filename": actual_file.name,
                        "page": page_num,
                        "img_index": img_idx,
                        "width": int(xobj_obj.get("/Width", 0)),
                        "height": int(xobj_obj.get("/Height", 0)),
                        "captions_on_page": captions_by_page.get(page_num, []),
                        "docs_path": f"/images/{actual_file.name}",
                    }
                    manifest.append(entry)
                    stats["images_extracted"] += 1
                    page_image_count += 1

                except Exception as e:
                    err = {"page": page_num, "name": str(name), "error": str(e)}
                    stats["errors"].append(err)

            if page_image_count > 0:
                stats["pages_with_images"] += 1

            if page_num % 50 == 0 or page_num == stats["total_pages"]:
                print(f"  page {page_num}/{stats['total_pages']} scanned", flush=True)

    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(
        json.dumps({"stats": stats, "images": manifest}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(f"\nDone. {stats['images_extracted']} images from {stats['pages_with_images']} pages.")
    print(f"Manifest: {manifest_path}")
    return stats


def main():
    ap = argparse.ArgumentParser(description="Extract images from Hacking the Xbox PDF")
    ap.add_argument("pdf", nargs="?", type=Path, default=DEFAULT_PDF)
    ap.add_argument("--out", type=Path, default=DEFAULT_IMAGES)
    ap.add_argument("--manifest", type=Path, default=MANIFEST_PATH)
    args = ap.parse_args()

    if not args.pdf.exists():
        print(f"ERROR: PDF not found at {args.pdf}", file=sys.stderr)
        sys.exit(1)

    extract(args.pdf, args.out, args.manifest)


if __name__ == "__main__":
    main()
