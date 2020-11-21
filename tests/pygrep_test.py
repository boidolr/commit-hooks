import re

import pytest
from pre_commit.clientlib import load_manifest
from pre_commit.constants import MANIFEST_FILE

HOOKS = {
    h["id"]: re.compile(h["entry"])
    for h in load_manifest(MANIFEST_FILE)
    if h["language"] == "pygrep"
}


@pytest.mark.parametrize(
    "s",
    (
        "tap((args) => console.log(args)),",
        "console.dir(obj);",
        "console.trace(data)",
        "console.info(data)",
        "console.warn(data)",
        "console.error(data)",
    ),
)
def test_ts_no_console_positive(s):
    assert HOOKS["ts-no-console"].search(s)


@pytest.mark.parametrize(
    "s",
    (
        "obj.console()",
        "obj.console.log()",
    ),
)
def test_ts_no_console_negative(s):
    assert not HOOKS["ts-no-console"].search(s)


@pytest.mark.parametrize(
    "s",
    (
        ")(window));",
        ' window.location = "/foo"',
        "window.onload = function() {",
    ),
)
def test_ts_no_window_positive(s):
    assert HOOKS["ts-no-window"].search(s)


@pytest.mark.parametrize(
    "s",
    (
        '"win" + "dow"',
        "this.window",
    ),
)
def test_ts_no_window_negative(s):
    assert not HOOKS["ts-no-window"].search(s)


@pytest.mark.parametrize(
    "s",
    (
        "tap(() => {debugger}),",
        "foo(); debugger;",
    ),
)
def test_ts_no_debugger_positive(s):
    assert HOOKS["ts-no-debugger"].search(s)


@pytest.mark.parametrize(
    "s",
    (
        'debug("function is ok")',
        'obj.debugger("method is ok")',
    ),
)
def test_ts_no_debugger_negative(s):
    assert not HOOKS["ts-no-debugger"].search(s)


@pytest.mark.parametrize(
    "s",
    (
        'fdescribe("focus block", () => ({}))',
        'xdescribe("ignore block", () => ({}))',
        'xdescribe ("ignore block with space", () => ({}))',
        'fit("focus case", () => ({}))',
        'xit("ignore case", () => ({}))',
        'xit ("ignore case with space", () => ({}))',
    ),
)
def test_ts_no_focus_ignore_positive(s):
    assert HOOKS["ts-no-focus-ignore"].search(s)


@pytest.mark.parametrize(
    "s",
    (
        'describe("block", () => {',
        'it("case", () => {',
    ),
)
def test_ts_no_focus_ignore_negative(s):
    assert not HOOKS["ts-no-focus-ignore"].search(s)
