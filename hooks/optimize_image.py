#!/usr/bin/env python3
import argparse
import sys
from pathlib import Path
from PIL import Image
from scour import scour
from typing import Sequence, Optional


def _optimize_jpeg_png(path: Path, quality: int) -> Path:
    bkp = path.with_suffix(path.suffix + '.bkp')
    im = Image.open(path)
    im.save(bkp, format=im.format, optimize=True, progressive=True, quality=quality)
    return bkp


def _optimize_svg(path: Path) -> Path:
    data = path.read_text()
    options = {
        'enable_viewboxing': True,
        'strip_ids': True,
        'strip_comments': True,
        'shorten_ids': True,
        'indent_type': 'none',
    }
    output = scour.scourString(data, options)

    bkp = path.with_suffix(path.suffix + '.bkp')
    bkp.write_text(output)
    return bkp


def _optimize_image(path: str, threshold: int, quality: int) -> None:
    fp = Path(path)

    if fp.suffix == '.svg':
        output = _optimize_svg(fp)
    else:
        output = _optimize_jpeg_png(fp, quality)

    original_size = fp.stat().st_size
    diff = original_size - output.stat().st_size
    if diff > threshold:
        output.replace(fp)
        print(f'optimized {path} by {diff} of {original_size} bytes')
    else:
        output.unlink()


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('filenames', nargs='*', help='Filenames to optimize.')
    parser.add_argument('-t', '--threshold', dest='threshold', default=1024, type=int,
                        help='Minimum improvment to replace file in bytes (default: %(default)s')
    parser.add_argument('-q', '--quality', dest='quality', default=80, type=int,
                        help='Quality to use for JPG images (default: %(default)s')
    args = parser.parse_args(argv)

    for file in args.filenames:
        try:
            _optimize_image(file, args.threshold, args.quality)
        except Exception as exc:
            print('Failed optimization for {} ({})'.format(','.join(args.filenames), exc), file=sys.stderr)
            return 1

    return 0


if __name__ == '__main__':
    sys.exit(main())
