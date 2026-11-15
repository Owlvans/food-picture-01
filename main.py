#!/usr/bin/env python3
import os
import sys
import hashlib

ENTRY_TITLE = "Double smash, cheese still falling"
EXPECTED_SHA256 = "91aee3016a77af81b9c0fdc9b8da7d712ea05719baf4711a8977641a98246fbc"
EXPECTED_BYTES = 241217

def check_image_truncation(data: bytes):
    if len(data) >= 2 and data[:2] == b'\xff\xd8':
        if len(data) < 2 or data[-2:] != b'\xff\xd9':
            raise ValueError("Invalid JPEG: file is truncated (missing EOI marker)")
    elif len(data) >= 8 and data[:8] == b'\x89PNG\r\n\x1a\n':
        if len(data) < 12 or data[-12:-8] != b'IEND':
            raise ValueError("Invalid PNG: file is truncated (missing IEND chunk)")
    else:
        raise ValueError("Unsupported image format (not JPEG or PNG)")

def get_image_dimensions(data: bytes):
    if len(data) >= 2 and data[:2] == b'\xff\xd8':
        if len(data) < 2 or data[-2:] != b'\xff\xd9':
            raise ValueError("Invalid JPEG: missing EOI marker")
        i = 2
        while i < len(data):
            if data[i] != 0xff:
                i += 1
                continue
            while i < len(data) and data[i] == 0xff:
                i += 1
            if i >= len(data):
                break
            marker = data[i]
            i += 1
            if marker == 0xd9 or (0xd0 <= marker <= 0xd7):
                break
            if marker == 0xd8:
                continue
            if i + 2 > len(data):
                break
            length = int.from_bytes(data[i:i+2], 'big')
            if 0xc0 <= marker <= 0xcf and marker not in (0xc4, 0xc8, 0xcc):
                if i + 7 > len(data):
                    raise ValueError("Invalid JPEG SOF segment")
                height = int.from_bytes(data[i+3:i+5], 'big')
                width = int.from_bytes(data[i+5:i+7], 'big')
                return width, height
            i += length
        raise ValueError("JPEG Start-Of-Frame (SOF) marker not found")
    elif len(data) >= 8 and data[:8] == b'\x89PNG\r\n\x1a\n':
        if len(data) < 24:
            raise ValueError("Invalid PNG: file too short")
        chunk_type = data[12:16]
        if chunk_type != b'IHDR':
            raise ValueError("Invalid PNG: first chunk is not IHDR")
        width = int.from_bytes(data[16:20], 'big')
        height = int.from_bytes(data[20:24], 'big')
        return width, height
    else:
        raise ValueError("Unsupported image format (not JPEG or PNG)")

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    pic_path = os.path.join(script_dir, "picture.jpg")

    if not os.path.exists(pic_path):
        print(f"Error: {pic_path} does not exist.", file=sys.stderr)
        sys.exit(1)

    size = os.path.getsize(pic_path)
    if size > 1048576:
        print(f"Error: File size {size} bytes exceeds maximum allowed (1048576 bytes).", file=sys.stderr)
        sys.exit(1)

    if size != EXPECTED_BYTES:
        print(f"Error: File size {size} bytes does not match expected {EXPECTED_BYTES} bytes.", file=sys.stderr)
        sys.exit(1)

    try:
        with open(pic_path, "rb") as f:
            data = f.read()
    except Exception as e:
        print(f"Error reading image file: {e}", file=sys.stderr)
        sys.exit(1)

    file_hash = hashlib.sha256(data).hexdigest()
    if file_hash != EXPECTED_SHA256:
        print(f"Error: SHA-256 hash {file_hash} does not match expected {EXPECTED_SHA256}.", file=sys.stderr)
        sys.exit(1)

    try:
        check_image_truncation(data)
        width, height = get_image_dimensions(data)
    except Exception as e:
        print(f"Error validating image: {e}", file=sys.stderr)
        sys.exit(1)

    if width > 1024 or height > 1024:
        print(f"Error: Dimensions {width}x{height} exceed maximum allowed (1024x1024).", file=sys.stderr)
        sys.exit(1)

    output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(output_dir, exist_ok=True)

    out_path = os.path.join(output_dir, "entry.png")
    with open(out_path, "wb") as f:
        f.write(data)

    source_hash = hashlib.sha256(data).hexdigest()
    with open(out_path, "rb") as f:
        output_data = f.read()
    output_hash = hashlib.sha256(output_data).hexdigest()

    print(f"Title: {ENTRY_TITLE}")
    print(f"Dimensions: {width}x{height}")
    print(f"Byte count: {size}")
    print(f"Source SHA-256: {source_hash}")
    print(f"Output SHA-256: {output_hash}")

    if source_hash != output_hash:
        print("Error: SHA-256 hash mismatch between source and output!", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
