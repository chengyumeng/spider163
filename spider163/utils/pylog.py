#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging

def Log(msg):
    logging.basicConfig(filename='spider163.log', level=logging.INFO)
    logging.info(msg)
