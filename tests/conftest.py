import pathlib
import pytest

from hooks.command_util import _execute_command


@pytest.fixture
def temp_git_dir(tmpdir):
    git_dir = tmpdir.join('gits')
    _execute_command('git', 'init', '--', git_dir.strpath)
    yield git_dir


@pytest.fixture
def dictionary_path():
    current_file = pathlib.Path(__file__).resolve()
    yield str(current_file.parent / 'words.json')
