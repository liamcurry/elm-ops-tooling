# elm-ops-tooling
Tooling for Elm ops


## elm_deps_check

Sometimes we need to make sure that two different exact-dependencies are the same. This is the case when you have a parent project, and a test project where the parent project dependencies are a sub list of test project.

Usage:

- `--exact` flag if you are passing `exact-dependencies.json`
- `--quiet` flag if you only want the error message

```bash

python elm_deps_check.py elm-stuff/exact-dependencies.json tests/elm-stuff/exact-dependencies.json --exact

```

will output

```bash
BUILD FAILED due to elm-deps mismatch, errors:
Package version mismatch for circuithub/elm-list-extra!

../NoRedInk/elm-stuff/exact-dependencies.json had 3.10.0
../NoRedInk/spec/elm/elm-stuff/exact-dependencies.json had 3.7.1
```

or

```bash
python elm_deps_check.py ../NoRedInk/elm-package.json ../NoRedInk/spec/elm/elm-package.json --quiet
```

## elm_deps_upgrade

Sometimes we want to figure out if our elm-package.json contains old deps.

Usage:

- `--elm-version` if you want to specify a different version of Elm. Defaults to 0.16

```bash

python elm_deps_upgrade.py elm-package.json

```

will print

```
Minors available for elm-lang/core: [2.1.0]
Majors available for elm-lang/core: [3.0.0]
Majors available for evancz/elm-html: [4.0.2, 4.0.1, 4.0.0]

```
