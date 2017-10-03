#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
from spider163.utils import config
from logbook import FileHandler, Logger

path = config.get_path()
log_handler = FileHandler(filename=path + '/spider163.log')
log_handler.push_application()
log = Logger("")


def Log(msg):
    log.warn(msg)