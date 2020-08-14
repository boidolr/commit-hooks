from hooks.search_replace import main


def test_unchanged_without_match(tmpdir):
    path = tmpdir.join('file')
    path.write('foo bar qux\nfirst second\n')

    with tmpdir.as_cwd():
        assert main((path.strpath, '-s', 'nothing', '-r', '')) == 0
        assert path.read_text('utf-8') == 'foo bar qux\nfirst second\n'


def test_replace_string_with_match(tmpdir):
    path = tmpdir.join('file')
    path.write('foo bar qux\nfirst second\n')

    with tmpdir.as_cwd():
        assert main((path.strpath, '-s', 'bar', '-r', 'cat')) == 1
        assert path.read_text('utf-8') == 'foo cat qux\nfirst second\n'


def test_replace_regex_with_match(tmpdir):
    path = tmpdir.join('file')
    path.write('foo bar qux\nfirst second\n')

    with tmpdir.as_cwd():
        assert main((path.strpath, '-s', '\\sbar\\s', '-r', '')) == 1
        assert path.read_text('utf-8') == 'fooqux\nfirst second\n'
