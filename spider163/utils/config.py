#!/usr/bin/env python
# -*- coding: utf-8 -*-

import ConfigParser

cf = ConfigParser.ConfigParser()
cf.read("../../spider163.conf")


def get_db():
    return cf.get("core", "db")


