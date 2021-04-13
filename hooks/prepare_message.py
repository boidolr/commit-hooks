#!/usr/bin/env python3
import argparse
import re
import sys
from operator import methodcaller
from pathlib import Path
from typing import Match
from typing import Optional
from typing import Pattern
from typing import Sequence

from .command_util import _execute_command


def _get_current_git_path() -> Optional[str]:
    return _execute_command("git", "rev-parse", "--git-path", ".")


def _git_op_in_progress() -> bool:
    git_dir = _get_current_git_path()
    if not git_dir:
        raise FileNotFoundError("Failed to find git directory")
    files = ("rebase-merge", "rebase-apply", "MERGE_HEAD", "MERGE_MSG")
    paths = map(Path(git_dir).joinpath, files)
    exists = map(methodcaller("exists"), paths)
    return any(exists)


def _get_branch_name() -> Optional[str]:
    return _execute_command("git", "symbolic-ref", "--short", "HEAD")


def _is_wrong_message_prefix(
    commit_msg_filepath: str, prefix_pattern: Pattern[str]
) -> bool:
    with open(commit_msg_filepath) as fh:
        commit_msg_start = fh.readline()
        return prefix_pattern.match(commit_msg_start) is None


def _update_message(
    commit_msg_filepath: str,
    branch_match: Optional[Match[str]],
    prefix_pattern: Pattern[str],
) -> bool:
    if branch_match is None:
        return False

    issue = branch_match.group(1)
    prefix = f"{issue}: "
    with open(commit_msg_filepath, "r+") as fh:
        commit_msg = fh.read()
        if not commit_msg.startswith((prefix, "Merge", "Revert", "fixup!", "squash!")):
            msg = prefix_pattern.sub("", commit_msg, count=1)
            fh.seek(0, 0)
            fh.write(prefix)
            fh.write(msg)
            fh.truncate()

    return True


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", help="Commit message file path")
    parser.add_argument(
        "--ignore-branch",
        nargs="*",
        dest="ignore_branch",
        help="Branches where no checking should be done.",
    )
    parser.add_argument(
        "--pattern",
        default=r"(?:feature|hotfix)\/(\w+-\d+)",
        help="Pattern to match feature branch name (default: %(default)s).",
    )
    parser.add_argument(
        "--prefix-pattern",
        default=r"^\s*\w+-\d+\s*:?\s*",
        dest="prefix",
        help="Pattern to match the commit message prefix (default: %(default)s).",
    )
    args = parser.parse_args(argv)

    if _git_op_in_progress():
        return 0

    branch_name = _get_branch_name()
    if branch_name is None:
        print("Not on a branch, returning early.", file=sys.stderr)
        return 1

    if args.ignore_branch is not None and branch_name in args.ignore_branch:
        return 0

    branch_name = branch_name.strip()
    match = re.match(args.pattern, branch_name)
    updated = _update_message(args.filename, match, re.compile(args.prefix))
    if not updated:
        print(f'Could not update message on branch "{branch_name}"', file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
