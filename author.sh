#!/bin/sh

git filter-branch --env-filter '

CORRECT_NAME="Kruttika Nadig"
CORRECT_EMAIL="kruttika17@gmail.com"

if [ "$GIT_COMMITTER_NAME" = "$CORRECT_NAME" ]
then
    export GIT_COMMITTER_EMAIL="$CORRECT_EMAIL"
fi
if [ "$GIT_AUTHOR_NAME" = "$CORRECT_NAME" ]
then
    export GIT_AUTHOR_EMAIL="$CORRECT_EMAIL"
fi
' --tag-name-filter cat -- --branches --tags