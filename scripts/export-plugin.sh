#!/usr/bin/env bash
set -euo pipefail

# Build the content-intelligence plugin .zip artifact.
# Usage:
#   ./scripts/export-plugin.sh           # release build, version from plugin.json
#   ./scripts/export-plugin.sh --preview # PR preview build, suffixed with PR + SHA

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

PREVIEW=0
if [ "${1:-}" = "--preview" ]; then
  PREVIEW=1
fi

# Read identity from plugin.json
NAME=$(jq -r '.name' .claude-plugin/plugin.json)
VERSION=$(jq -r '.version' .claude-plugin/plugin.json)

if [ -z "$NAME" ] || [ -z "$VERSION" ] || [ "$NAME" = "null" ] || [ "$VERSION" = "null" ]; then
  echo "ERROR: plugin.json missing name or version"
  exit 1
fi

# Validate manifests
echo "Validating manifests..."
jq . .claude-plugin/plugin.json > /dev/null || { echo "ERROR: plugin.json is invalid JSON"; exit 1; }
jq . .claude-plugin/marketplace.json > /dev/null || { echo "ERROR: marketplace.json is invalid JSON"; exit 1; }

# Validate skill frontmatter
echo "Validating skill frontmatter..."
shopt -s nullglob
for f in skills/*/SKILL.md; do
  if ! head -1 "$f" | grep -q '^---$'; then
    echo "ERROR: missing frontmatter (must start with '---'): $f"
    exit 1
  fi
done
shopt -u nullglob

# Determine output filename
SUFFIX=""
if [ "$PREVIEW" = "1" ]; then
  SHA="${GITHUB_SHA:-$(git rev-parse HEAD 2>/dev/null || echo 'nogit')}"
  SHORT_SHA="${SHA:0:7}"
  PR="${GITHUB_PR_NUMBER:-local}"
  SUFFIX="-pr${PR}-${SHORT_SHA}"
fi

mkdir -p dist
OUTFILE="dist/${NAME}-${VERSION}${SUFFIX}.zip"

# Stage to temp dir (guard the cleanup trap so it never runs with an empty TMP)
TMP=$(mktemp -d)
trap 'if [ -n "${TMP:-}" ] && [ -d "$TMP" ]; then rm -rf "$TMP"; fi' EXIT
STAGE="$TMP/${NAME}"
mkdir -p "$STAGE"

echo "Staging files..."
rsync -a \
  --exclude='.git' \
  --exclude='.gitignore' \
  --exclude='.claude' \
  --exclude='dist' \
  --exclude='node_modules' \
  --exclude='.DS_Store' \
  --exclude='*.log' \
  --exclude='.worktrees' \
  --exclude='.changeset' \
  --exclude='.github' \
  --exclude='package.json' \
  --exclude='package-lock.json' \
  --exclude='scripts' \
  --exclude='docs/superpowers' \
  --exclude='docs/plans' \
  --exclude='SUBMISSION_CHECKLIST.md' \
  ./ "$STAGE/"

# Strip .gitkeep
find "$STAGE" -name '.gitkeep' -delete

# Drop empty directories left behind by exclusions (e.g., docs/ when only superpowers/ existed)
find "$STAGE" -type d -empty -delete

# Defensive guard: bail if the empty-dir prune unexpectedly removed the
# staging root. Should never happen because $STAGE has content from
# rsync, but if it does we want a clear error rather than a confusing
# zip failure.
if [ ! -d "$STAGE" ]; then
  echo "ERROR: staging directory was unexpectedly removed"
  exit 1
fi

# Zip (clean overwrite if the file already exists)
echo "Building $OUTFILE..."
rm -f "$OUTFILE"
(cd "$TMP" && zip -rq "${REPO_ROOT}/${OUTFILE}" "${NAME}/")

# SHA256
if command -v sha256sum >/dev/null 2>&1; then
  SHA256=$(sha256sum "$OUTFILE" | awk '{print $1}')
else
  SHA256=$(shasum -a 256 "$OUTFILE" | awk '{print $1}')
fi

echo ""
echo "Built: $OUTFILE"
echo "SHA256: $SHA256"
