#!/usr/bin/env python3
import argparse
import sys
from pathlib import Path
from PIL import Image
from typing import Sequence, Optional


def _optimize_pillow(path: Path) -> Path:
    bkp = path.with_suffix(path.suffix + ".bkp")
    im = Image.open(path)
    im.save(bkp, format=im.format, optimize=True)
    return bkp


def optimize_png(path: str, threshold: int) -> None:
    fp = Path(path)
    output = _optimize_pillow(fp)

    original_size = fp.stat().st_size
    diff = original_size - output.stat().st_size
    if diff > threshold:
        output.replace(fp)
        print(
            f"Optimized {path} by {diff} of {original_size} bytes ({diff/original_size:.2%})"
        )
    else:
        output.unlink()


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("filenames", nargs="*", help="Files to optimize.")
    parser.add_argument(
        "-t",
        "--threshold",
        default=1024,
        type=int,
        help="Minimum improvement to replace file in bytes (default: %(default)s)",
    )
    args = parser.parse_args(argv)

    for file in args.filenames:
        try:
            optimize_png(file, args.threshold)
        except Exception as exc:
            print(
                f"Failed optimization for {file} ({exc})",
                file=sys.stderr,
            )
            return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
