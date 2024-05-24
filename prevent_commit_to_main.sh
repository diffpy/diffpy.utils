#!/bin/sh
##!"C:\\Program Files\\Git\\usr\\bin\\bash.exe"

branch="$(git rev-parse --abbrev-ref HEAD)"

if [ "$branch" = "main" ]; then
echo "You are on the main branch. Committing to the main branch is not allowed."
exit 1
fi
