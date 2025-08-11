#!/bin/bash

if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" ]]; then
    REPO_PATH="$PWD"
else
    REPO_PATH="$HOME/src"
fi

cd "$REPO_PATH" || exit 1

git fetch origin main || exit 1
git reset --hard origin/main || exit 1

