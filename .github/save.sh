#!/usr/bin/env bash
set -u
git config user.name "copybot"
git config user.email "copybot@users.noreply.github.com"
git add -A
git diff --cached --quiet && { echo "nothing to save"; exit 0; }
git commit -qm "$1 $(date -u +%Y-%m-%dT%H:%MZ)"
for i in 1 2 3 4 5; do
  git pull -q --rebase -X theirs origin main && git push -q origin HEAD:main && exit 0
  sleep $((i * 5))
done
echo "push failed"; exit 1
