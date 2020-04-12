import pytest

from hooks.spellcheck_message import main


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        ('Fixnga bug', 'Fixing bug'),
        ('And a longr mesage', 'And a long message'),
    ),
)
def test_suggests_correct_message(input_s, expected, tmpdir, capsys):
    path = tmpdir.join('message')
    path.write(input_s)
    assert main((path.strpath,)) == 1
    corrected = capsys.readouterr().out
    assert expected in corrected


@pytest.mark.parametrize(
    ('input_s',),
    (
        ('',),
        ('Same message',),
    ),
)
def test_keeps_correct_message(input_s, tmpdir, capsys):
    path = tmpdir.join('message')
    path.write(input_s)
    assert main((path.strpath,)) == 0
    corrected = capsys.readouterr().out
    assert '' == corrected


@pytest.mark.parametrize(
    ('input_s', 'expected', 'unexpected'),
    (
        ('One line\nTwo lnies', 'Two lines', 'One line'),
        ('One line with white space\n\n\nCorrected lnie', 'Corrected line', 'One line'),
    ),
)
def test_print_only_fixed_line(input_s, expected, unexpected, tmpdir, capsys):
    path = tmpdir.join('message')
    path.write(input_s)
    assert main((path.strpath,)) == 1
    corrected = capsys.readouterr().out
    assert expected in corrected
    assert unexpected not in corrected
