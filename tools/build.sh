#!/bin/bash
set -e
. .env/bin/activate

echo "Build python package..."
python3 setup.py sdist bdist_wheel
