#!/bin/bash
set -e
. .env/bin/activate
mathy_pydoc mathy_core.tokenizer.Tokenizer++ mathy_core.parser++ mathy_core.tree++ mathy_core.expressions++ mathy_core.rules.associative_swap++ mathy_core.rules.balanced_move++ mathy_core.rules.commutative_swap++ mathy_core.rules.constants_simplify++ mathy_core.rules.distributive_factor_out++ mathy_core.rules.distributive_multiply_across++ mathy_core.rules.variable_multiply++ mathy_core.layout++ mathy_core.problems++ > /tmp/pathy_api.md
python3 tools/docs.py /tmp/pathy_api.md README.md
npx prettier README.md --write