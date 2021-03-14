import subprocess  # nosec
import typing


def _execute_command(
    *args: str, returncode: typing.Optional[int] = None
) -> typing.Optional[str]:
    result = subprocess.run(  # nosec
        args, encoding="utf-8", stderr=subprocess.DEVNULL, stdout=subprocess.PIPE
    )
    if (
        returncode is None
        and result.returncode != 0
        or returncode is not None
        and result.returncode != returncode
    ):
        return None
    return result.stdout.strip()
