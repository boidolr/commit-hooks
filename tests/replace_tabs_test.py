from hooks.replace_tabs import main


def test_unchanged_without_match(tmp_path):
    path = tmp_path / "file"
    path.write_text("foo bar qux\nfirst second\n")

    main((str(path),)) == 0
    assert path.read_text("utf-8") == "foo bar qux\nfirst second\n"


def test_replace_tabs(tmp_path):
    path = tmp_path / "file"
    path.write_text("foo\tbar qux\n\t\tfirst second\n")

    assert main((str(path),)) == 1
    assert path.read_text("utf-8") == "foo    bar qux\n        first second\n"


def test_replace_with_changed_size(tmp_path):
    path = tmp_path / "file"
    path.write_text("foo\tbar qux\n\t\tfirst second\n")

    assert main((str(path), "-t", "2")) == 1
    assert path.read_text("utf-8") == "foo  bar qux\n    first second\n"
