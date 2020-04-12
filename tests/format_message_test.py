import pytest

from hooks.format_message import main


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        ('', ''),
        ('foobar', 'foobar'),
        ('foo\nbar', 'foo\n\n\nbar'),
        ('bar\n\nbaz', 'bar\n\n\nbaz'),
        ('baz\n\n\nqux', 'baz\n\n\nqux'),
        ('baz\n\n\n\nqux', 'baz\n\n\nqux'),
    ),
)
def test_fixes_heading_message_distance(input_s, expected, tmpdir):
    path = tmpdir.join('message')
    path.write(input_s)
    assert main((path.strpath,)) == 0
    assert path.read() == expected
