#!/usr/bin/env python
# -*- coding: utf-8 -*-

import contextlib
from spider163 import version


@contextlib.contextmanager
def ignored(*exceptions):
    try:
        yield
    except exceptions:
        pass


def encode(s):
    if version.PYTHON3 is True:
        return str(s)
    else:
        return s.encode("utf-8")

