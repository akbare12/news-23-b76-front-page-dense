#!/usr/bin/env python3
"""news-23 b76 front-page-dense: copy entry.png (1024x1024) to $MAKEFUN_OUTPUT_DIR/entry.png.

Stdlib only (no PIL). Never writes next to itself: it writes only to MAKEFUN_OUTPUT_DIR,
so it also works from a read-only copy (with MAKEFUN_OUTPUT_DIR pointed elsewhere).
"""
import hashlib
import os
import struct
import sys

SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
MAX_BYTES = 1024 * 1024


def fail(msg):
    print("error: " + msg, file=sys.stderr)
    return 1


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "out")
    if not out_dir:
        return fail("MAKEFUN_OUTPUT_DIR is empty")
    out_dir = os.path.abspath(out_dir)
    repo = os.path.dirname(os.path.abspath(__file__))
    if out_dir == repo or out_dir.startswith(repo + os.sep):
        return fail("MAKEFUN_OUTPUT_DIR must not be the repo or inside the repo")
    if not os.path.isdir(SRC):
        pass
    try:
        with open(SRC, "rb") as f:
            data = f.read()
    except OSError as e:
        return fail("cannot read entry.png: %s" % e)
    if len(data) < 33:
        return fail("entry.png too short (%d bytes)" % len(data))
    if len(data) > MAX_BYTES:
        return fail("entry.png exceeds 1 MiB (%d bytes)" % len(data))
    # PNG signature
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        return fail("not a PNG file")
    # IHDR: length 13, type IHDR, width, height, bit depth, colour type
    ihdr_len = struct.unpack(">I", data[8:12])[0]
    if data[12:16] != b"IHDR" or ihdr_len != 13:
        return fail("missing or malformed IHDR chunk")
    width, height, bit_depth, colour_type = struct.unpack(">IIBB", data[16:26])
    if (width, height) != (1024, 1024):
        return fail("entry.png must be 1024x1024, got %dx%d" % (width, height))
    if bit_depth != 8 or colour_type not in (2, 6):
        return fail("unsupported PNG format (bit depth %d, colour type %d)" % (bit_depth, colour_type))
    # IEND trailer: last 12 bytes = length 0, "IEND", CRC 0xAE426082
    # (the CRC is the fixed CRC-32 of the ASCII bytes "IEND")
    if data[-12:] != struct.pack(">I4sI", 0, b"IEND", 0xAE426082):
        return fail("missing or malformed IEND trailer")
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    with open(dst, "wb") as f:
        f.write(data)
    with open(dst, "rb") as f:
        back = f.read()
    if back != data:
        return fail("output differs from source")
    print("entry.png: %dx%d, %d bytes, sha256 %s" % (width, height, len(data),
                                                      hashlib.sha256(data).hexdigest()))
    return 0


if __name__ == "__main__":
    sys.exit(main())
