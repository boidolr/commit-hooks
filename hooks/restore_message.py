#!/usr/bin/env python3
import argparse
import pathlib
import shutil
import sys
import typing

from .util import _execute_command


def _get_backup_file_path() -> typing.Optional[str]:
    return _execute_command('git', 'rev-parse', '--git-path', 'PRECOMMIT_COMMIT_EDITMSG')


def _restore_message(backup_file: str, message_file: str) -> None:
    backup_path = pathlib.Path(backup_file)
    if not backup_path.exists():
        return

    message_path = pathlib.Path(message_file)
    message_content = message_path.read_text(encoding='utf-8')

    whitespace_or_comments = not any(
        not line.isspace()
        for line in message_content.splitlines()
        if not line.startswith('#')
    )
    if len(message_content) == 0 or whitespace_or_comments:
        backup_content = backup_path.read_text(encoding='utf-8')
        lines = [line for line in backup_content.splitlines() if not line.startswith('#')]
        with message_path.open('w') as fh:
            fh.write('# last commit message:\n# ')
            fh.write('\n# '.join(lines))
            fh.write('\n')
            fh.write(message_content)


def _save_message(backup_file: str, message_file: str) -> None:
    shutil.copyfile(message_file, backup_file)


def main(argv: typing.Optional[typing.Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', '--mode', choices=('save', 'restore'),
                        help='Whether to save or restore the commit message content')
    parser.add_argument('filename', help='Commit message file path')
    args = parser.parse_args(argv)

    backup_file = _get_backup_file_path()

    if backup_file is None:
        return 1

    if args.mode == 'save':
        _save_message(backup_file, args.filename)
    else:
        _restore_message(backup_file, args.filename)

    return 0


if __name__ == '__main__':
    sys.exit(main())
