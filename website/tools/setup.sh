#!/bin/bash
set -e

# Make the virtualenv only if the folder doesn't exist
DIR=../../.env
if [ ! -d "${DIR}" ]; then
  sh ../../tools/setup.sh
fi

# Use root env
. ../../.env/bin/activate
echo "Installing/updating requirements..."
pip install -r requirements.txt
