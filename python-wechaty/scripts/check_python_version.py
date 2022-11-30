#!/usr/bin/env python3
"""check version"""

import re
import sys
from typing import Tuple


def version() -> Tuple[int, int, int]:
    """version"""
    try:
        ver = re.findall(r'^\d+\.\d+\.\d+', sys.version)[0]
        senior, minor, patch = re.findall(r'\d+', ver)
        return (int(senior), int(minor), int(patch))

    # pylint: disable=W0703
    except Exception:
        return (0, 0, 0)


# major, minor, patch = version()


if sys.version_info < (3, 6):
    sys.exit('ERROR: Python 3.7 or above is required.')
else:
    print('Python %d.%d.%d passed checking.' % sys.version_info[:3])
