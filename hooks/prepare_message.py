#!/usr/bin/env python3
import argparse
import re
import sys
import typing

from .util import _execute_command


def _get_branch_name() -> typing.Optional[str]:
    return _execute_command('git', 'symbolic-ref', '--short', 'HEAD')


def _is_wrong_message_prefix(commit_msg_filepath: str) -> bool:
    with open(commit_msg_filepath, 'r') as fh:
        commit_msg_start = fh.readline()
        return re.match(r'^\s*\w+-\d+\s*:?\s*', commit_msg_start) is None


def _update_message(branch: str, commit_msg_filepath: str) -> bool:
    match = re.match(r'(?:feature|hotfix)\/(\w+-\d+)', branch)

    if match is None:
        return False

    issue = match.group(1)
    prefix = '{}: '.format(issue)
    with open(commit_msg_filepath, 'r+') as fh:
        commit_msg = fh.read()
        if not commit_msg.startswith((prefix, 'Merge', 'Revert')):
            msg = re.sub(r'^\s*\w+-\d+\s*:?\s*', '', commit_msg, count=1)
            fh.seek(0, 0)
            fh.write(prefix)
            fh.write(msg)
            fh.truncate()

    return True


def main(argv: typing.Optional[typing.Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', help='Commit message file path')
    args = parser.parse_args(argv)

    branch_name = _get_branch_name()
    if branch_name is None:
        print('Not on a branch, returning early.', file=sys.stderr)
        return 1

    if branch_name in ('master', 'develop'):
        if _is_wrong_message_prefix(args.filename):
            print('On "{}" with invalid prefix'.format(branch_name), file=sys.stderr)
            return 1
        else:
            return 0

    updated = _update_message(branch_name, args.filename)
    if not updated:
        print('Could not update message on branch "{}"'.format(branch_name), file=sys.stderr)
        return 1

    return 0


if __name__ == '__main__':
    sys.exit(main())
