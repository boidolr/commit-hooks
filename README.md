pre-commit-hooks
================

Some hooks for pre-commit.

See also: https://github.com/pre-commit/pre-commit

[![Build Status](https://travis-ci.org/boidolr/pre-commit-hooks.svg?branch=master)](https://travis-ci.org/boidolr/pre-commit-hooks)

### Using pre-commit-hooks with pre-commit

Add this to your `.pre-commit-config.yaml`

    -   repo: https://github.com/boidolr/pre-commit-hooks
        rev: v1.1.0  # Use the ref you want to point at
        hooks:
        -   id: console-logging
        # -   id: ...


### Hooks available

#### Commit message related

- `prepare-message`: Change commit messages to include a ticket prefix.
- `check-message`: Ensure commit message conforms to format of headline followed by two empty lines.
- `save-message`: Save commit message - hook needs to be used in conjunction with `restore-message`.
    In case the commit is aborted during processing this hook enables saving the content of the commit message.
    It needs to be included as first hook in the processing chain.
- `restore-message`: Restore commit message - hook needs to be used in conjunction with `save-message`.
    In case the previous commit was aborted this hook restores the content of the commit message into the editor.

#### Code related

- `check-test`: Remove focus and ignore from [jasmine](https://jasmine.github.io/) and [jest](https://jestjs.io/) tests.
- `ng-lint`: Execute `ng lint --fix` from the `node_module` directory for changed files.
- `console-logging`: Remove lines containing javascript console statements.
- `properties-whitespace`: Remove whitespace around equal signs in property files.
