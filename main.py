#!/usr/bin/env python3
"""news-image-20261121 — front page for Saturday 21 November 2026.

The finished picture is part of this repository (assets/entry.png). This
program only validates it and copies it to the grader's output directory,
so it needs no network and every run writes exactly the same bytes.

Run:  MAKEFUN_OUTPUT_DIR=out python3 main.py
"""
from __future__ import annotations

import hashlib
import os
import struct
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCE = HERE / "assets" / "entry.png"
MAX_BYTES = 1_048_576
MAX_SIDE = 1024
SIGNATURE = b"\x89PNG\r\n\x1a\n"


def fail(reason: str) -> "SystemExit":
    print(f"main.py: {reason}", file=sys.stderr)
    return SystemExit(1)


def inspect(data: bytes) -> tuple[int, int]:
    """Reject anything that is not a small, well-formed PNG."""
    if len(data) > MAX_BYTES:
        raise fail(f"entry.png is {len(data)} bytes, over the 1 MiB cap")
    if data[:8] != SIGNATURE:
        raise fail("entry.png is not a PNG file")
    if len(data) < 33 or data[12:16] != b"IHDR":
        raise fail("entry.png has no IHDR chunk")
    w, h = struct.unpack(">II", data[16:24])
    if w > MAX_SIDE or h > MAX_SIDE:
        raise fail(f"entry.png is {w}x{h}, over the 1024x1024 cap")
    if w == 0 or h == 0:
        raise fail("entry.png has a zero dimension")
    return w, h


def run() -> int:
    data = SOURCE.read_bytes()
    width, height = inspect(data)

    out = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out.mkdir(parents=True, exist_ok=True)
    dest = out / "entry.png"
    dest.write_bytes(data)

    again = dest.read_bytes()
    if again != data:
        raise fail("written file differs from the repository artwork")

    print(f"entry.png {width}x{height} {len(data)} bytes "
          f"sha256={hashlib.sha256(data).hexdigest()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(run())
