"""Gate checks for the entry: image limits and byte-identical reruns."""
import hashlib
import os
import struct
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))


def png_size(path):
    with open(path, "rb") as f:
        head = f.read(24)
    assert head[:8] == b"\x89PNG\r\n\x1a\n", "not a PNG"
    w, h = struct.unpack(">II", head[16:24])
    return w, h


def run_once():
    with tempfile.TemporaryDirectory() as td:
        env = dict(os.environ, MAKEFUN_OUTPUT_DIR=td)
        subprocess.run([sys.executable, os.path.join(HERE, "main.py")],
                       env=env, check=True, capture_output=True)
        with open(os.path.join(td, "entry.png"), "rb") as f:
            return f.read()


def main():
    img = os.path.join(HERE, "news.png")
    data = open(img, "rb").read()
    assert len(data) <= 1048576, f"image too big: {len(data)}"
    assert png_size(img) == (1024, 1024), "image must be 1024x1024"
    a, b = run_once(), run_once()
    assert a == b, "two runs differ"
    assert hashlib.sha256(a).hexdigest() == hashlib.sha256(data).hexdigest(), \
        "output must equal the committed news.png"
    print("all entry checks pass:", len(data), "bytes")


if __name__ == "__main__":
    main()
