#!/usr/bin/env python3
import argparse
import sys
from pathlib import Path
from typing import Sequence, Optional

from .optimize_jpg import optimize_jpg
from .optimize_png import optimize_png
from .optimize_svg import optimize_svg
from .optimize_webp import optimize_webp


def _optimize_image(path: str, threshold: int, quality: int) -> None:
    suffix = Path(path).suffix.lower()
    if suffix == ".svg":
        optimize_svg(path, threshold)
    elif suffix == ".png":
        optimize_png(path, threshold)
    elif suffix == ".webp":
        optimize_webp(path, threshold, True, 80)
    elif suffix == ".jpg" or suffix == ".jpeg":
        optimize_jpg(path, threshold, quality)
    else:
        raise Exception("Unknown image suffix", suffix)


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("filenames", nargs="*", help="File names to optimize.")
    parser.add_argument(
        "-t",
        "--threshold",
        default=1024,
        type=int,
        help="Minimum improvement to replace file in bytes (default: %(default)s)",
    )
    parser.add_argument(
        "-q",
        "--quality",
        default=80,
        type=int,
        help="Quality to use for JPG images (default: %(default)s)",
    )
    args = parser.parse_args(argv)

    for file in args.filenames:
        try:
            _optimize_image(file, args.threshold, args.quality)
        except Exception as exc:
            print(
                f"Failed optimization for {file} ({exc})",
                file=sys.stderr,
            )
            return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
