#!/usr/bin/env python3
import argparse
import sys

from autocorrect import Speller, word_regexes
from difflib import ndiff
from re import sub
from typing import Optional, Sequence


def _check_message_spelling(commit_msg_filepath: str, language: str) -> int:
    spell = Speller(lang=language)
    with open(commit_msg_filepath, 'r') as fh:
        content = fh.read()

        correction = spell(content)
        if correction == content:
            return 0

        print('Spell check failed:')
        before = sub(r'\n{2,}', '\n', content)
        after = sub(r'\n{2,}', '\n', correction)

        for old, new in zip(before.splitlines(), after.splitlines()):
            if old == new:
                continue

            print('\n'.join(ndiff([old], [new])))

        return 1


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', help='Commit message file path')
    parser.add_argument(
        '-l', '--language',
        default='en',
        choices=sorted(word_regexes.keys()),
        help='Language to use for spellchecking (default: %(default)s)')
    args = parser.parse_args(argv)

    return _check_message_spelling(args.filename, args.language)


if __name__ == '__main__':
    sys.exit(main())
