#!/bin/bash
for file in $(git diff --name-only && git ls-files --others --exclude-standard); do
  git add "$file"
  git commit -m "Add $file"
  git push origin chore/rename-filesystem-according-to-project
done