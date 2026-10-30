#!/usr/bin/env bash
# Bump the version, commit, push and create a GitHub release (which publishes to PyPI).
#
# Usage: scripts/release.sh [major|minor|patch]   (default: minor)
set -euo pipefail

bump="${1:-minor}"
case "$bump" in
  major|minor|patch) ;;
  *) echo "Usage: $0 [major|minor|patch]" >&2; exit 1 ;;
esac

cd "$(git rev-parse --show-toplevel)"

if [[ "$(git branch --show-current)" != "main" ]]; then
  echo "Releases must be created from 'main'." >&2
  exit 1
fi

if [[ -n "$(git status --porcelain)" ]]; then
  echo "Working tree is not clean, commit or stash your changes first." >&2
  exit 1
fi

git fetch origin main
if [[ "$(git rev-parse HEAD)" != "$(git rev-parse origin/main)" ]]; then
  echo "Local 'main' is not in sync with 'origin/main'." >&2
  exit 1
fi

uv version --bump "$bump"
version="$(uv version --short)"
tag="v$version"

git commit -m "Release $tag" pyproject.toml uv.lock
git push origin main

gh release create "$tag" --target main --title "$tag" --generate-notes

echo "Released $tag, the publish workflow is running now."
