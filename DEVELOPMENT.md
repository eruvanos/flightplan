# Development

## Setup

The project is managed with [uv](https://docs.astral.sh/uv/).
Supported Python versions are 3.11 and higher (see `requires-python` in `pyproject.toml`).

```bash
uv sync               # create .venv with all dependencies (incl. dev group)
uv run fp --help      # run the CLI from the working tree
```

The default branch is `main`.

## Tests

```bash
uv run pytest           # run the tests
uv run -p 3.11 pytest   # run the tests with a specific Python version
```

Note: the round trip tests rewrite the YAML fixtures in `tests/data` in place
(anchors are resolved, keys sorted). Check `git status` after running them and
do not commit unintended fixture changes.

## CI

`.github/workflows/workflow.yml` runs on pushes to `main`, pull requests and published releases:

1. `test` – runs the test suite on all supported Python versions
2. `build` – builds sdist and wheel with `uv build`
3. `publish` – only for published GitHub releases, uploads to PyPI via
   [trusted publishing](https://docs.pypi.org/trusted-publishers/) (GitHub environment `pypi`)

## Release a new version

1. Make sure `main` is green in CI.
2. Bump the version:
   ```bash
   uv version --bump patch   # or minor / major, updates pyproject.toml and uv.lock
   ```
3. Optionally verify the build locally:
   ```bash
   uv build
   ```
4. Commit and push:
   ```bash
   git commit -am "Release vX.Y.Z"
   git push origin main
   ```
5. Create a GitHub release with a matching tag, e.g.:
   ```bash
   gh release create vX.Y.Z --target main --generate-notes
   ```
6. Publishing the release triggers the workflow, which tests, builds and uploads
   the package to [PyPI](https://pypi.org/p/flightplan). Check the run under the
   repository's *Actions* tab.

A version can only be uploaded to PyPI once. If publishing fails after the upload,
bump the version again instead of re-using it.
