#!/usr/bin/env python3
"""
crop_figures.py — Deterministic figure-cropping tool.

Reads source/figure-crops.json, crops the specified pixel boxes out of
existing page-render PNGs (docs/public/images/page-NNN-render.png), and
writes the cropped figure-only PNGs to docs/public/images/figures/.

This script does NOT touch Markdown files and does NOT delete any source
page-render files. It only generates cropped images from a manifest, so
crop coordinates are always recorded and reproducible.

Usage:
    python3 scripts/crop_figures.py
    python3 scripts/crop_figures.py --manifest source/figure-crops.json
    python3 scripts/crop_figures.py --only ch01-fig1-1 ch01-fig1-2
"""

import argparse
import json
import sys
from pathlib import Path

try:
    from PIL import Image
except ImportError:
    sys.exit("ERROR: Pillow is required (pip install Pillow --break-system-packages)")

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_MANIFEST = REPO_ROOT / "source" / "figure-crops.json"


def load_manifest(path: Path) -> dict:
    if not path.exists():
        sys.exit(f"ERROR: manifest not found: {path}")
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def crop_entry(entry: dict) -> Path:
    entry_id = entry["id"]
    source_render = REPO_ROOT / entry["source_render"]
    output_image = REPO_ROOT / entry["output_image"]
    box_type = entry.get("box_type", "pixel")
    box = entry["box"]
    source_size = entry.get("source_size")

    if not source_render.exists():
        raise FileNotFoundError(f"[{entry_id}] source render not found: {source_render}")

    im = Image.open(source_render)
    actual_size = list(im.size)

    if source_size is not None and actual_size != list(source_size):
        raise ValueError(
            f"[{entry_id}] source_size mismatch: manifest says {source_size}, "
            f"actual render is {actual_size}. Re-check crop coordinates before proceeding."
        )

    if box_type == "normalized":
        w, h = im.size
        left, top, right, bottom = box
        pixel_box = (int(left * w), int(top * h), int(right * w), int(bottom * h))
    elif box_type == "pixel":
        pixel_box = tuple(int(v) for v in box)
    else:
        raise ValueError(f"[{entry_id}] unknown box_type: {box_type!r}")

    left, top, right, bottom = pixel_box
    if not (0 <= left < right <= im.size[0] and 0 <= top < bottom <= im.size[1]):
        raise ValueError(f"[{entry_id}] crop box {pixel_box} is out of bounds for image size {im.size}")

    cropped = im.crop(pixel_box)
    output_image.parent.mkdir(parents=True, exist_ok=True)
    cropped.save(output_image)
    return output_image


def main():
    parser = argparse.ArgumentParser(description="Crop figure images from page renders per manifest.")
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST, help="Path to figure-crops.json")
    parser.add_argument("--only", nargs="*", default=None, help="Only process these entry ids")
    args = parser.parse_args()

    manifest = load_manifest(args.manifest)
    entries = manifest.get("crops", [])

    if args.only:
        wanted = set(args.only)
        entries = [e for e in entries if e["id"] in wanted]
        missing = wanted - {e["id"] for e in entries}
        if missing:
            sys.exit(f"ERROR: unknown entry id(s): {sorted(missing)}")

    if not entries:
        print("No crop entries to process.")
        return

    generated = []
    errors = []
    for entry in entries:
        try:
            out_path = crop_entry(entry)
            generated.append((entry["id"], out_path))
        except Exception as e:
            errors.append((entry["id"], str(e)))

    print(f"Processed {len(entries)} manifest entr{'y' if len(entries) == 1 else 'ies'}.")
    print(f"Generated {len(generated)} file(s):")
    for entry_id, path in generated:
        rel = path.relative_to(REPO_ROOT)
        print(f"  [{entry_id}] {rel}")

    if errors:
        print(f"\n{len(errors)} error(s):")
        for entry_id, msg in errors:
            print(f"  [{entry_id}] {msg}")
        sys.exit(1)


if __name__ == "__main__":
    main()
