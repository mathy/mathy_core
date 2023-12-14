#!/bin/bash
set -e

# Default Python path
PYTHON_PATH="python3"

# Check if a custom Python path is provided as the first argument
if [ -n "$1" ]; then
  PYTHON_PATH="$1"
fi

echo "Using Python at: $PYTHON_PATH"
$PYTHON_PATH --version

# Make the virtualenv only if the folder doesn't exist
DIR=.env
if [ ! -d "${DIR}" ]; then
  pip install virtualenv --upgrade
  $PYTHON_PATH -m virtualenv .env -p $PYTHON_PATH || virtualenv .env -p $PYTHON_PATH
fi

echo "Installing/updating requirements..."
.env/bin/pip install -r requirements.txt
.env/bin/mkdocs build
