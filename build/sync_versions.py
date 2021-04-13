#!/usr/bin/env python3
import fileinput
import re
import sys
import typing


def main(source: str, targets: typing.Iterable[str]) -> None:
    with open(source) as fh:
        dependency_versions = [
            line.strip().split("==") for line in fh.readlines() if "==" in line
        ]
        versions = [
            (re.compile(v[0] + r"==[^\s,\]]+"), v[0] + "==" + v[1])
            for v in dependency_versions
        ]

    with fileinput.input(files=targets, inplace=True) as files:
        for line in files:
            for pattern, replacement in versions:
                line = pattern.sub(replacement, line)
            print(line, end="")


if __name__ == "__main__":
    if len(sys.argv) <= 2:
        sys.exit(f"Need more arguments: python3 {__file__} source targets...")

    source = sys.argv[1]
    targets = sys.argv[2:]
    main(source, targets)
