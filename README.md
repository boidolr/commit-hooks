pre-commit-hooks
================

Some hooks for pre-commit.

See also: https://github.com/pre-commit/pre-commit


### Using pre-commit-hooks with pre-commit

Add this to your `.pre-commit-config.yaml`

    -   repo: https://github.com/boidolr/pre-commit-hooks
        rev: v1.0.0  # Use the ref you want to point at
        hooks:
        -   id: console-logging
        # -   id: ...


### Hooks available

- `console-logging`: Remove lines containing javascript console statements.
- `properties-whitespace`: Remove whitespace around equal signs in property files.
- `prepare-message`: Change commit messages to include a ticket prefix.
- `check-message`: Ensure commit message conforms to format of headline followed by two empty lines.
- `check-test`: Remove focus and ignore from [jasmine](https://jasmine.github.io/) and [jest](https://jestjs.io/) tests.
