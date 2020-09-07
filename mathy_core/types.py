import sys

# Use typing_extensions for Python < 3.8
if sys.version_info < (3, 8):
    from typing_extensions import Literal, Final  # noqa
else:
    from typing import Literal, Final  # noqa
