#!/bin/sh -e
. .env/bin/activate

# Sort imports one per line, so autoflake can remove unused imports
isort mathy_core tests --force-single-line-imports
autoflake --remove-all-unused-imports --recursive --remove-unused-variables --in-place mathy_core tests --exclude=__init__.py
isort mathy_core tests
black mathy_core tests