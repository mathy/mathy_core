#!/bin/bash
set -e
echo "Activating virtualenv... (if this fails you may need to run setup.sh first)"
echo "Running tests..."
../.env/bin/python3 -m pytest --cov=mathy_core
