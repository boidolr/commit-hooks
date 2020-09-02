import pytest

from hooks.prepare_message import main
from hooks.command_util import _execute_command


def test_abort_when_no_branch(temp_git_dir):
    path = temp_git_dir.join("message")
    path.write("")
    with temp_git_dir.as_cwd():
        # not on a branch
        _execute_command("git", "checkout", "--detach", "HEAD")
        assert main((path.strpath,)) == 1
        assert path.read() == ""


def test_ignore_merge(temp_merge_conflict):
    message = temp_merge_conflict.join("message")
    message.write("")
    path = temp_merge_conflict.join("file")
    with temp_merge_conflict.as_cwd():
        assert main((path.strpath,)) == 0
        assert message.read() == ""


def test_ignore_rebase(temp_rebase_conflict):
    message = temp_rebase_conflict.join("message")
    message.write("")
    path = temp_rebase_conflict.join("file")
    with temp_rebase_conflict.as_cwd():
        assert main((path.strpath,)) == 0
        assert message.read() == ""


@pytest.mark.parametrize(
    ("branch", "content", "return_code"),
    (
        ("develop", "foo", 1),
        ("master", "foo", 0),
    ),
)
def test_handle_ignored_branch(branch, content, return_code, temp_git_dir):
    path = temp_git_dir.join("message")
    path.write(content)
    with temp_git_dir.as_cwd():
        # now on branch
        _execute_command("git", "checkout", "-b", branch)
        assert (
            main(
                (
                    "--ignore-branch=master",
                    path.strpath,
                )
            )
            == return_code
        )
        assert path.read() == content


@pytest.mark.parametrize(
    ("branch", "content", "expected", "return_code"),
    (
        ("feature/JIRA-1", "foo", "JIRA-1: foo", 0),
        ("hotfix/JIRA-2", "JIRA-2 foo", "JIRA-2: foo", 0),
        ("feature/JIRA-3", "JIRA-3: foo", "JIRA-3: foo", 0),
        ("feature/JIRA-4", "JIRA-4 : foo", "JIRA-4: foo", 0),
        ("feature/JIRA-5", " JIRA-5: foo", "JIRA-5: foo", 0),
    ),
)
def test_handle_prefix_on_feature_branch(
    branch, content, expected, return_code, temp_git_dir
):
    path = temp_git_dir.join("message")
    path.write(content)
    with temp_git_dir.as_cwd():
        # now on branch
        _execute_command("git", "checkout", "-b", branch)
        assert main((path.strpath,)) == return_code
        assert path.read() == expected
