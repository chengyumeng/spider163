#!/usr/bin/env python
# -*- coding: utf-8 -*-

import contextlib
import codecs
import requests
import json
import hashlib
from bs4 import BeautifulSoup

from spider163 import version
from spider163.utils import const


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


def md5(s):
    m = hashlib.md5()
    m.update(s.encode("utf-8"))
    return m.hexdigest()


def curl(url, headers, type = const.RETURN_JSON):
    try:
        s = requests.session()
        bs = BeautifulSoup(s.get(url, headers=headers).content, "html.parser")
        if type == const.RETURN_JSON:
            return json.loads(bs.text)
        elif type == const.RETURE_HTML:
            return bs
        else:
            return bs.text
    except Exception:
        raise

