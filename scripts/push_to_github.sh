#!/usr/bin/env bash
set -euo pipefail

REPO_URL="${1:-git@github.com:GLGr13/chora-vex-artifacts.git}"
BRANCH="${2:-main}"

if [ ! -d .git ]; then
  git init
fi

git checkout -B "$BRANCH"
git add .
git commit -m "Initialize CHORA public repository shell" || true
git remote remove origin 2>/dev/null || true
git remote add origin "$REPO_URL"
git push -u origin "$BRANCH"
