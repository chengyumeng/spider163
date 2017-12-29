#!/usr/bin/env python
# -*- coding: utf-8 -*-

from spider163 import settings
from spider163.utils import pylog
try:
    settings.configure_orm()
except Exception as e:
    pylog.print_info("无法执行数据库相关的任务： {}".format(e))