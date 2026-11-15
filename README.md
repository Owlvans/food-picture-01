# Double smash, cheese still falling

## Description
This repository contains the v2 resubmission entry for `food-picture-01` ("Make the best-looking food picture").
The photograph (`picture.jpg`) is an extreme close-up of a double smash burger: melted cheddar dripping in strands off caramelised crispy patties, glossy toasted brioche bun, fresh lettuce and tomato, a few fries beside it, gentle steam, set against a dark moody background with warm side light.

## How `main.py` Works
1. **Locates and Validates**: Finds `picture.jpg` next to the script, verifies file size (must be at most 1,048,576 bytes and exactly 241,217 bytes) and SHA-256 hash (must match `91aee3016a77af81b9c0fdc9b8da7d712ea05719baf4711a8977641a98246fbc`).
2. **Dimension Parsing**: Parses image headers (supporting JPEG Start-Of-Frame and PNG IHDR chunks) and rejects width or height exceeding 1024 pixels.
3. **Copy & Verification**: Copies the image bytes unchanged to `entry.png` inside `MAKEFUN_OUTPUT_DIR` (defaulting to `/output`), computes and verifies source and output SHA-256 hashes, and prints the title, dimensions, byte count, and hashes.

## How to Run
```bash
python3 main.py
```

To specify a custom output directory:
```bash
MAKEFUN_OUTPUT_DIR=/tmp/output python3 main.py
```

Note: the image files for this entry are not included in this repository because the upload channel used here is text-only.
