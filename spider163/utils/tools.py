#!/usr/bin/env python
# -*- coding: utf-8 -*-

import contextlib
import codecs
from spider163 import version


@contextlib.contextmanager
def ignored(*exceptions):
    try:
        yield
    except exceptions:
        pass


def encode(s):
    if version.PYTHON3 is True:
        return codecs.encode(s,"utf-8").decode("utf-8")
    else:
        return s.encode("utf-8")


def hex(s):
    if version.PYTHON3 is True:
        return codecs.encode(bytes(s, encoding = "utf8"), 'hex')
    else:
        return s.encode("hex")

