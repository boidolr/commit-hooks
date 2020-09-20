pre-commit-hooks [![tag](https://img.shields.io/github/v/tag/boidolr/pre-commit-hooks)](https://github.com/boidolr/pre-commit-hooks/tags) [![Build Status](https://github.com/boidolr/pre-commit-hooks/workflows/CI/badge.svg?branch=master)](https://github.com/boidolr/pre-commit-hooks/actions) [![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)
================

Some hooks for [pre-commit](https://github.com/pre-commit/pre-commit).

See also: https://github.com/pre-commit/pre-commit-hooks


### Using pre-commit-hooks with pre-commit

Add this to your `.pre-commit-config.yaml`

    -   repo: https://github.com/boidolr/pre-commit-hooks
        rev: v2.6  # Use the ref you want to point at
        hooks:
        -   id: console-logging
        # -   id: ...


### Hooks available

#### Commit message related

- `prepare-message`: Change commit messages to include a prefix.
    - `--ignore-branch` will lead to the branch not being checked.
    - `--pattern` can be used to change the feature branch pattern to take the message prefix from.
        Needs to match with `--prefix-pattern`. Defaults to `feature/(\w+-\d+)`.
    - `--prefix-pattern` should match the prefix of the message to normalize it.
        Needs to match with `--pattern`. Defaults to `^\s*\w+-\d+\s*:`
- `format-message`: Ensure commit message conforms to format of headline followed by two empty lines.
    - `--capitalize` if the subject line should be capitalized. Other lines remain unchanged.
- `spellcheck-message`: Test the message against a known dictionary.
    - `--language` can be used to switch to other supported languages then English (`en`).
    - `--dictionary` will specify a (non-default) dictionary to be used with autocorrect. The format is a JSON (string, integer) file.
- `restore-message`: Restore commit message.
    In case the previous commit was aborted this hook restores the content of `COMMIT_EDITMSG` the commit message into the editor.
    Similar to `git commit --reuse-message=.git/COMMIT_EDITMSG`.

#### Code related

- `check-test`: Check for focus and ignore of [jasmine](https://jasmine.github.io/) and [jest](https://jestjs.io/) tests.
- `ng-lint`: Execute `ng lint` for changed files only.
    - `--fix` will call `ng lint` with `--fix`.
    - `--ng-path` can be used to give the path to the `ng` executable. Default is `node_modules/.bin/ng`.
- `optimize-image`: Compress `png`, `jpeg` and `svg` images. Specific hooks are available for fine grained configuration.
    - `--threshold` can be used to configure which size difference should be used to keep the image.
    - `--quality` can be used to configure quality setting for a JPG image.
- `optimize-jpg`: Compress `jpeg` images.
    - `--threshold` can be used to configure which size difference should be used to keep the image.
    - `--quality` can be used to configure quality setting for a JPG image.
- `optimize-png`: Compress `png` images.
    - `--threshold` can be used to configure which size difference should be used to keep the image.
- `optimize-svg`: Compress `svg` images.
    - `--threshold` can be used to configure which size difference should be used to keep the image.
- `optimize-webp`: Compress `webp` images.
    - `--threshold` can be used to configure which size difference should be used to keep the image.
    - `--lossless` switch to lossless compession.
    - `--quality` can be used to configure quality setting for lossy compression or effort to spend on lossless compression.
- `replace-tabs`: Replace tabs in files.
    - `--tabsize`: spaces to replace a tab with.
- `search-replace`: Replace patterns in files.
    - `--search`: regular expression to use for search.
    - `--replacement`: replacement for matches.
- `console-debugger`: Check for lines containing JavaScript `debugger` statements.
- `console-logging`: Check for lines containing JavaScript `console` logging statements.
- `console-window`: Check for lines containing JavaScript `window` statements.
- `properties-whitespace`: Remove whitespace around equal signs in property files.


### References

Some of the hooks only work because of other projects:

- [autocorrect](https://github.com/fsondej/autocorrect)
- [PIL](https://github.com/python-pillow/Pillow)
- [scour](https://github.com/scour-project/scour)
