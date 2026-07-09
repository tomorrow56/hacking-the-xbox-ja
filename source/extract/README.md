# source/extract/

This directory is populated by running the extraction scripts:

```
python3 scripts/extract_text.py
python3 scripts/extract_images.py
```

**Prerequisites:**
1. Place `source/HackingTheXbox_Free.pdf` (free edition from https://nostarch.com/xboxfree)
2. Install PyMuPDF: `pip install pymupdf`

## Directory layout after extraction

```
source/extract/
  pages/
    page-001.txt  ... page-NNN.txt   # one file per PDF page
  images/
    page-PPP-img-NN.png / .jpeg      # embedded images
  figures-manifest.json               # image index with captions
  text-extract-summary.json           # extraction stats
```
