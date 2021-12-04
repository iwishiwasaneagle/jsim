#!/usr/bin/env bash

# takes the tag as an argument (e.g. v0.1.0)
if [ -n "$1" ]
then

    if ! command -v pre-commit &>/dev/null
    then
        echo "error: pre-commit is not in PATH. This will cause issues with this script."
        exit 1
    fi

    pre-commit uninstall
    git-cliff --tag "$1" > CHANGELOG.md
    git commit CHANGELOG.md -m "chore(release): prepare for $1"
    git show
    # generate a changelog for the tag message
    export TEMPLATE="\
    {% for group, commits in commits | group_by(attribute=\"group\") %}
    {{ group | upper_first }}\
    {% for commit in commits %}
    	- {{ commit.message | upper_first }} ({{ commit.id | truncate(length=7, end=\"\") }})\
    {% endfor %}
    {% endfor %}"
    changelog=$(git-cliff --unreleased --strip all)
    # create a signed tag
    # https://keyserver.ubuntu.com/pks/lookup?search=0x4A92FA17B6619297&op=vindex
    git tag -s -a "$1" -m "Release $1" -m "$changelog"
    git tag -v "$1"
    git push origin "$1"
    pre-commit install
else
    echo "warn: please provide a tag"
fi
