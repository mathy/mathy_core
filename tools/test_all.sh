#!/bin/bash
set -e

sh tools/test.sh
(cd website && sh tools/test.sh)
