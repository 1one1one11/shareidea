#!/usr/bin/env bash
set -euo pipefail

MESSAGE="${1:-docs: update static site}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

cd "${REPO_ROOT}"

echo "[deploy] Building docs..."
python scripts/build_docs.py

echo "[deploy] Staging changes..."
git add .

if [[ -z "$(git status --porcelain)" ]]; then
  echo "[deploy] No changes to commit."
  exit 0
fi

echo "[deploy] Committing..."
git commit -m "${MESSAGE}"

echo "[deploy] Pushing..."
git push

echo "[deploy] Completed."
