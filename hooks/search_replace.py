#!/usr/bin/env python3
import argparse
import re
import sys

from typing import Optional, Pattern, Sequence


def _search_replace(filename: str, pattern: Pattern[str], replacement: str) -> int:
    with open(filename, 'r') as fh:
        content = fh.readlines()

    ret = 0
    for index, line in enumerate(content):
        processed = pattern.sub(replacement, line)
        if processed != line:
            print(f'{filename}:{index + 1}:', end='')
            print(line)
            content[index] = processed
            ret = 1

    if ret != 0:
        with open(filename, 'w') as fh:
            fh.writelines(content)

    return ret


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
        ret |= _search_replace(filename, pattern, args.replacement)
    return ret


if __name__ == '__main__':
    sys.exit(main())
