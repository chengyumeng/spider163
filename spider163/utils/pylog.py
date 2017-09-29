#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
from spider163.utils import config


def Log(msg):
    path = config.get_path()
    logging.basicConfig(filename=path + '/spider163.log', level=logging.INFO)
    logging.info(msg)
