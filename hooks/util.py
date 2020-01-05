import subprocess
import sys


def _execute_command(*args):
    try:
        return subprocess.check_output(args, encoding='utf-8').strip()
    except subprocess.CalledProcessError as e:
        print('Failed to execute command', str(args), str(e), file=sys.stderr)
        return None
