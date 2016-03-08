# elm-ops-tooling
Tooling for Elm ops


## elm_deps_check

Sometimes we need to make sure that two different exact-dependencies are the same. This is the case when you have a parent project, and a test project where the parent project dependencies are a sub list of test project.

Usage:

```bash

python elm-stuff/exact-dependencies.json tests/elm-stuff/exact-dependencies.json

```
