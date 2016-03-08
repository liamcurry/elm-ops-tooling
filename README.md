# elm-ops-tooling
Tooling for Elm ops


## elm_deps_check

Sometimes we need to make sure that two different exact-dependencies are the same. This is the case when you have a parent project, and a test project where the parent project dependencies are a sub list of test project.

Usage:

```bash

python elm-stuff/exact-dependencies.json tests/elm-stuff/exact-dependencies.json

```

## elm_deps_upgrade

Sometimes we want to figure out if our elm-package.json contains old deps.

```bash

python elm_deps_upgrade.py elm-package.json

```

will print

```
Minors available for elm-lang/core: [2.1.0]
Majors available for elm-lang/core: [3.0.0]
Majors available for evancz/elm-html: [4.0.2, 4.0.1, 4.0.0]

```
