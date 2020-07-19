import sys

# Use typing_extensions for Python < 3.8
if sys.version_info < (3, 8):
    from typing_extensions import Final, Literal  # noqa
else:
    from typing_extensions import Final, Literal  # noqa

