from hooks.restore_message import main


def test_message_is_saved(temp_git_dir):
    path = temp_git_dir.join('message')
    path.write('commit message')
    with temp_git_dir.as_cwd():
        assert main(('--mode', 'save', path.strpath,)) == 0
        assert temp_git_dir.join('.git/PRECOMMIT_COMMIT_EDITMSG').read() == 'commit message'


def test_message_is_added_to_current_message_when_empty(temp_git_dir):
    path = temp_git_dir.join('message')
    path.write('')
    temp_git_dir.join('.git/PRECOMMIT_COMMIT_EDITMSG').write('previous message')
    with temp_git_dir.as_cwd():
        assert main(('--mode', 'restore', path.strpath,)) == 0
        assert path.read() == '# last commit message:\n# previous message\n'


def test_message_is_added_to_current_message_when_only_comments(temp_git_dir):
    path = temp_git_dir.join('message')
    path.write('# some git stuff')
    temp_git_dir.join('.git/PRECOMMIT_COMMIT_EDITMSG').write('previous message')
    with temp_git_dir.as_cwd():
        assert main(('--mode', 'restore', path.strpath,)) == 0
        assert path.read() == '# last commit message:\n# previous message\n# some git stuff'


def test_message_is_not_added_to_current_message_when_already_filled(temp_git_dir):
    path = temp_git_dir.join('message')
    path.write('commit message')
    temp_git_dir.join('.git/PRECOMMIT_COMMIT_EDITMSG').write('previous message')
    with temp_git_dir.as_cwd():
        assert main(('--mode', 'restore', path.strpath,)) == 0
        assert path.read() == 'commit message'
