import re

import pytest
from pre_commit.clientlib import load_manifest
from pre_commit.constants import MANIFEST_FILE

HOOKS = {
    h['id']: re.compile(h['entry']) for h in load_manifest(MANIFEST_FILE) if h['language'] == 'pygrep'
}


@pytest.mark.parametrize(
    's',
    (
        'tap(() => {debugger;}),',
        'foo(); debugger;',
    ),
)
def test_console_debugger_positive(s):
    assert HOOKS['console-debugger'].search(s)


@pytest.mark.parametrize(
    's',
    (
        'debug()',
        '"debugging"',
    ),
)
def test_console_debugger_negative(s):
    assert not HOOKS['console-debugger'].search(s)


@pytest.mark.parametrize(
    's',
    (
        'tap((args) => console.log(args)),',
        'console.dir(obj);',
        'console.trace(data)',
        'console.info(data)',
        'console.warn(data)',
        'console.error(data)',
    ),
)
def test_console_logging_positive(s):
    assert HOOKS['console-logging'].search(s)


@pytest.mark.parametrize(
    's',
    (
        'console.time("obj");',
        'console.timeEnd("obj")',
        'console.group(data)',
    ),
)
def test_console_logging_negative(s):
    assert not HOOKS['console-logging'].search(s)


@pytest.mark.parametrize(
    's',
    (
        ')(window));',
        ' window.location = "/foo"',
        'window.onload = function() {',
    ),
)
def test_console_window_positive(s):
    assert HOOKS['console-window'].search(s)


@pytest.mark.parametrize(
    's',
    (
        '"win" + "dow"',
    ),
)
def test_console_window_negative(s):
    assert not HOOKS['console-window'].search(s)


@pytest.mark.parametrize(
    's',
    (
        'fdescribe("focus", () => {',
        'xdescribe("ignore", () => {',
        'fit("focus", () => {',
        'xit("ignore", () => {',
    ),
)
def test_check_test_positive(s):
    assert HOOKS['check-test'].search(s)


@pytest.mark.parametrize(
    's',
    (
        'describe("block", () => {',
        'it("case", () => {',
    ),
)
def test_check_test_negative(s):
    assert not HOOKS['check-test'].search(s)
