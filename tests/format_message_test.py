import pytest

from hooks.format_message import main


@pytest.mark.parametrize(
    ("input_s", "expected"),
    (
        ("", ""),
        ("foobar", "foobar"),
        ("foo\nbar", "foo\n\n\nbar"),
        ("bar\n\nbaz", "bar\n\n\nbaz"),
        ("baz\n\n\nqux", "baz\n\n\nqux"),
        ("baz\n\n\n\nqux", "baz\n\n\nqux"),
    ),
)
def test_fixes_heading_message_distance(input_s, expected, tmp_path):
    path = tmp_path / "message"
    path.write_text(input_s)
    assert main((str(path),)) == 0
    assert path.read_text("utf-8") == expected


@pytest.mark.parametrize(
    ("input_s", "expected"),
    (
        ("", ""),
        ("foobar", "Foobar"),
        ("foo\n\n\nbar", "Foo\n\n\nbar"),
    ),
)
def test_capitalizes_subject(input_s, expected, tmp_path):
    path = tmp_path / "message"
    path.write_text(input_s)
    assert main((str(path), "-c")) == 0
    assert path.read_text("utf-8") == expected
