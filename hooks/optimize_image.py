#!/usr/bin/env python3
import argparse
import sys
from pathlib import Path
from PIL import Image
from scour import scour
from typing import Sequence, Optional


def _optimize_jpeg_png(path: Path, threshold: int) -> Path:
    # JPEG: quality=0..100
    bkp = path.with_suffix(path.suffix + '.bkp')
    im = Image.open(path)
    im.save(bkp, format=im.format, optimize=True, progressive=True)
    return bkp


def _optimize_svg(path: Path, threshold: int) -> Path:
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


def _optimize_image(path: str, threshold: int) -> None:
    fp = Path(path)

    if fp.suffix == '.svg':
        output = _optimize_svg(fp, threshold)
    else:
        output = _optimize_jpeg_png(fp, threshold)

    if fp.stat().st_size > output.stat().st_size + threshold:
        output.replace(fp)
    else:
        output.unlink()


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('filenames', nargs='*', help='Filenames to optimize.')
    parser.add_argument('--threshold', dest='threshold', default=128, type=int,
                        help='Minimum improvment to replace file in bytes (default: %(default)s')
    args = parser.parse_args(argv)

    for file in args.filenames:
        try:
            _optimize_image(file, args.threshold)
        except Exception as exc:
            print('Failed optimization for {} ({})'.format(','.join(args.filenames), exc))
            return 1

    return 0


if __name__ == '__main__':
    sys.exit(main())
