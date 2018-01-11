#!/usr/bin/env python
# -*- coding: utf-8 -*-

import contextlib


@contextlib.contextmanager
def ignored(*exceptions):
    try:
        yield
    except exceptions:
        pass
