#!/usr/bin/env python3
import argparse
import re
import sys

from typing import Optional, Pattern, Sequence


def _search_replace(filename: str, pattern: Pattern[str], replacement: str) -> int:
    with open(filename, 'r') as fh:
        content = fh.readlines()
        processed = [pattern.sub(replacement, line) for line in content]

    if content != processed:
        with open(filename, 'w') as fh:
            for line in processed:
                fh.write(line)
        return 1

    return 0


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('filenames', nargs='*', help='Filenames to search')
    parser.add_argument(
        '-s', '--search', dest='pattern',
        help='Regular expression to use for search')
    parser.add_argument(
        '-r', '--replacement',
        help='Replacement for successful matches')
    args = parser.parse_args(argv)

    ret = 0
    pattern = re.compile(args.pattern)
    for filename in args.filenames:
        code = _search_replace(filename, pattern, args.replacement)
        if code == 1:
            print(f'Replaced in {filename}')
            ret = 1
    return ret


if __name__ == '__main__':
    sys.exit(main())
