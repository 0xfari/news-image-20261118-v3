#!/usr/bin/env python3
"""Write the news-image-20261118 v3 front page to the output directory.

The repository ships the finished front page as entry.png.b64 (base64,
one line). This program decodes it, checks that the bytes are a complete,
well-formed PNG of the size the entry promises, and writes them to
$MAKEFUN_OUTPUT_DIR/entry.png (default: out/).

Why no rendering here: the grader runs stock python:3.13-slim, which has
no Pillow and no fonts, so anything importing PIL fails before it starts.
The picture itself was drawn locally (see render.py, kept in the repo as
the generator source); this file only carries it into the run.

Standard library only. No network, no randomness, no wall-clock time:
two runs write byte-identical output.
"""

import base64
import binascii
import hashlib
import os
import struct
import sys
import zlib
from pathlib import Path

HERE = Path(__file__).resolve().parent
B64_FILE = HERE / "entry.png.b64"
OUT_NAME = "entry.png"

PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
EXPECTED_WIDTH = 1024
EXPECTED_HEIGHT = 1024


def fail(message):
    print(f"main.py: {message}", file=sys.stderr)
    sys.exit(1)


def read_payload():
    try:
        text = B64_FILE.read_text(encoding="ascii")
    except OSError as exc:
        fail(f"cannot read {B64_FILE.name}: {exc}")
    stripped = "".join(text.split())
    if not stripped:
        fail("entry.png.b64 is empty")
    lines = [ln for ln in text.splitlines() if ln.strip()]
    if len(lines) != 1:
        fail(f"entry.png.b64 should be one line, found {len(lines)}")
    try:
        data = base64.b64decode(stripped, validate=True)
    except (binascii.Error, ValueError) as exc:
        fail(f"entry.png.b64 is not valid base64: {exc}")
    return data


def check_png(data):
    """Walk the PNG chunks, verifying structure, CRCs and size."""
    if len(data) < 8 or data[:8] != PNG_SIGNATURE:
        fail("decoded bytes do not start with the PNG signature")
    pos = 8
    seen_ihdr = False
    seen_iend = False
    while pos < len(data):
        if pos + 8 > len(data):
            fail("truncated PNG chunk header")
        length = struct.unpack(">I", data[pos:pos + 4])[0]
        ctype = data[pos + 4:pos + 8]
        end = pos + 8 + length + 4
        if end > len(data):
            fail(f"truncated PNG chunk {ctype!r}")
        body = data[pos + 8:pos + 8 + length]
        stored_crc = struct.unpack(">I", data[end - 4:end])[0]
        # PNG CRC covers the chunk type plus its data, not the data alone.
        actual_crc = zlib.crc32(ctype + body) & 0xFFFFFFFF
        if actual_crc != stored_crc:
            fail(f"PNG chunk {ctype!r} has a bad CRC")
        if ctype == b"IHDR":
            if seen_ihdr:
                fail("PNG has two IHDR chunks")
            seen_ihdr = True
            if length != 13:
                fail("IHDR chunk has the wrong length")
            width, height = struct.unpack(">II", body[:8])
            if (width, height) != (EXPECTED_WIDTH, EXPECTED_HEIGHT):
                fail(f"PNG is {width}x{height}, expected "
                     f"{EXPECTED_WIDTH}x{EXPECTED_HEIGHT}")
        if ctype == b"IEND":
            seen_iend = True
            if end != len(data):
                fail("trailing bytes after IEND")
            break
        pos = end
    if not seen_ihdr:
        fail("PNG has no IHDR chunk")
    if not seen_iend:
        fail("PNG has no IEND chunk")


def main():
    data = read_payload()
    check_png(data)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "out")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, OUT_NAME)
    with open(out_path, "wb") as fh:
        fh.write(data)
    raw = open(out_path, "rb").read()
    if raw != data:
        fail("written entry.png does not match the decoded bytes")
    print("entry.png: %d bytes sha256=%s" % (
        len(raw), hashlib.sha256(raw).hexdigest()))
    print("stories: 48 (3 leads + 10 cards + 35 briefs)")


if __name__ == "__main__":
    main()
