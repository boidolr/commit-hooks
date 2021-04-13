import pathlib

import pytest

from hooks.command_util import _execute_command


@pytest.fixture
def temp_git_dir(tmpdir):
    git_dir = tmpdir.join("gits")
    git_dir.mkdir()
    _execute_command("git", "init", "--", str(git_dir))
    yield git_dir


@pytest.fixture
def temp_merge_conflict(temp_git_dir):
    with temp_git_dir.as_cwd():
        path = temp_git_dir.join("file")
        path.write("")
        _execute_command("git", "config", "user.name", "tester")
        _execute_command("git", "config", "user.email", "tester@local")
        _execute_command("git", "add", "file")
        _execute_command("git", "commit", "-am", "inital")
        path.write("first")
        _execute_command("git", "commit", "-am", "first")
        _execute_command("git", "checkout", "-b", "develop", "HEAD~1")
        path.write("second")
        _execute_command("git", "commit", "-am", "second")

        _execute_command("git", "merge", "master")
        assert "<<<<<<< HEAD" in path.read()
    yield temp_git_dir


@pytest.fixture
def temp_rebase_conflict(temp_git_dir):
    with temp_git_dir.as_cwd():
        path = temp_git_dir.join("file")
        path.write("")
        _execute_command("git", "config", "user.name", "tester")
        _execute_command("git", "config", "user.email", "tester@local")
        _execute_command("git", "add", "file")
        _execute_command("git", "commit", "-am", "inital")
        path.write("first")
        _execute_command("git", "commit", "-am", "first")
        _execute_command("git", "checkout", "-b", "develop", "HEAD~1")
        path.write("second")
        _execute_command("git", "commit", "-am", "second")

        _execute_command("git", "rebase", "master")
        assert "<<<<<<< HEAD" in path.read()

    yield temp_git_dir


@pytest.fixture
def dictionary_path():
    current_file = pathlib.Path(__file__).resolve()
    yield str(current_file.parent / "words.json")
