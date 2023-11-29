#!/bin/bash
set -e

# Make the virtualenv only if the folder doesn't exist
DIR=.env
if [ ! -d "${DIR}" ]; then
  pip install virtualenv --upgrade
  python3 -m virtualenv .env -p python3
fi

. .env/bin/activate
echo "Installing/updating requirements..."
pip install -e .[all]