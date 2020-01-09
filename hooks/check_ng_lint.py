#!/usr/bin/env python3
import argparse
import sys

from typing import Sequence, Optional
from .util import _execute_command


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('filenames', nargs='*', help='Filenames to check.')
    args = parser.parse_args(argv)

    command = ['node_modules/.bin/ng', 'lint', '--fix']
    if len(args.filenames) > 0:
        command.extend(['--files', ','.join(args.filenames)])

    try:
        _execute_command(*command)
    except Exception as exc:
        print('Failed execute ng lint for {} ({})'.format(','.join(args.filenames), exc))
        return 1
    else:
        return 0


if __name__ == '__main__':
    sys.exit(main())
