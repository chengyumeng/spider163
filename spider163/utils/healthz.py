#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import json
from sqlalchemy import func

from spider163.utils import config
from spider163.utils import pylog
from spider163.utils import pysql
from spider163 import settings


def is_correct_config():
    pylog.print_info("正在检查配置路径：{}".format(config.PATH))
    if not os.path.exists(config.PATH + "/spider163.conf"):
        print("  - 配置路径下 spider163.conf {}".format(pylog.red("不存在")))
    else:
        print("  - 配置路径下 spider163.conf {}".format(pylog.green("存在")))
    pylog.print_info("正在检查配置文件 {}/spider163.conf 内容是否完整".format(config.PATH))
    try:
        config.cf.get("core", "db")
        print("  - 配置文件中 db   选项      {}".format(pylog.green("存在")))
    except Exception:
        print("  - 配置文件中 db   选项      {}".format(pylog.red("不存在")))
    try:
        config.cf.get("core", "port")
        print("  - 配置文件中 port 选项      {}".format(pylog.green("存在")))
    except Exception:
        print("  - 配置文件中 port 选项      {}".format(pylog.red("不存在")))


def is_correct_db():
    db = config.format_db()
    pylog.print_info("正在检查配置的数据库格式和可用性")
    if db is None:
        print("  - 配置文件中 db 选项  {}".format(pylog.red("不正确")))
    else:
        print("  - 账号：{} 密码：{} IP：{} 数据库：{}".format(db["user"], db["password"], db["ip"], db["database"]))
        try:
            from sqlalchemy import create_engine
            create_engine(db["link"], echo=False).execute("show databases")
            print("数据库连接验证                {}".format(pylog.green("成功")))
        except Exception as e:
            pylog.print_err("数据库连接失败，上述配置信息有问题: {}".format(e))


def can_spider():
    print("抓取验证未完成")


def expose_data():
    playlist = settings.Session.query(pysql.Playlist163).count()
    playlist_type = settings.Session.query(pysql.Playlist163, func.count(pysql.Playlist163.id)).group_by(pysql.Playlist163.id).all()
    music = settings.Session.query(pysql.Music163).count()
    comment = settings.Session.query(pysql.Comment163).count()
    lyric = settings.Session.query(pysql.Lyric163).count()
    top = settings.Session.query(pysql.Toplist163).count()
    data = {'playlist': {'count': playlist},
            'music': {'count': music,},
            'comment': {'count': comment},
            'lyric': {'count': lyric},
            'top':{'count': top}
        }
    js = json.dumps(data, ensure_ascii=False, indent=2)
    print(js)