import sys
from typing import Union

# Use typing_extensions for Python < 3.8
if sys.version_info < (3, 8):
    from typing_extensions import Literal  # noqa
else:
    from typing import Literal  # noqa

NumberType = Union[float, int]

__all__ = ("NumberType", "Literal")
