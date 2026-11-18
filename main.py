"""Entry point for news-image-20261118 (round 2).

The picture itself is drawn by render.py (Pillow) at build time and committed
as news.png; this program runs in the grading sandbox with the standard
library only, so it copies the committed image to the output path. Two runs
write byte-identical files because the source never changes.
"""
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "news.png")


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(SRC, dst)
    print("wrote", dst)


if __name__ == "__main__":
    main()
