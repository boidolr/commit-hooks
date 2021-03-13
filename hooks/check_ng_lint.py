#!/usr/bin/env python3
import argparse
import sys
from typing import Sequence, Optional
from .command_util import _execute_command


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("filenames", nargs="*", help="File names to check.")
    parser.add_argument(
        "--fix", action="store_true", help="Use ng lint to fix issues where possible."
    )
    parser.add_argument(
        "--ng-path",
        dest="path",
        default="node_modules/.bin/ng",
        help="Path to `ng` executable (default: %(default)s",
    )
    args = parser.parse_args(argv)

    command = [args.path, "lint"]

    if args.fix:
        command.append("--fix")

    if len(args.filenames) > 0:
        command.extend(["--files", ",".join(args.filenames)])

    try:
        _execute_command(*command)
    except Exception as exc:
        print(
            "Failed execute ng lint for {} ({})".format(",".join(args.filenames), exc),
            file=sys.stderr,
        )
        return 1
    else:
        return 0


if __name__ == "__main__":
    sys.exit(main())
