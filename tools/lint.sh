#!/usr/bin/env bash

set -e
. .env/bin/activate

echo "========================= mypy"
mypy mathy_core
echo "========================= flake8"
flake8 mathy_core tests
echo "========================= black"
black mathy_core tests --check
echo "========================= pyright"
npx pyright mathy_core tests