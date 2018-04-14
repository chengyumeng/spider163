#!/usr/bin/env python
# -*- coding: utf-8 -*-

from spider163 import settings
from spider163 import version
from spider163.spider import public as uapi
from spider163.utils import pysql
from spider163.utils import pylog
from spider163.utils import mail
from spider163.utils import config


def music(playlist_id):
    if playlist_id not in uapi.top.keys():
        pylog.print_info("歌单 {} 不在合法排行榜序列,合法歌单如下".format(playlist_id))
        tb = [['歌单ID','歌单名字']]
        for k,v in uapi.top.items():
            tb.append([k, v])
        pylog.Table(tb)
        return
    data = settings.Session.query(
        pysql.Toplist163.song_name,
        pysql.Toplist163.song_id,
        pysql.Toplist163.author,
        pysql.Toplist163.comment.label("count")
    ).filter(pysql.Toplist163.playlist_id == playlist_id, pysql.Toplist163.mailed == "N").order_by(pysql.Toplist163.id.asc()).slice(1,5).all()

    page = []
    body = version.MAILBODY
    title = version.MAILMUSIC
    comments = version.MAILCOMMENT
    for m in data:
        settings.Session.query(pysql.Toplist163).filter(pysql.Toplist163.song_id == m[1]).update({'mailed': 'Y'})
        settings.Session.commit()
        detail = ""
        cms = settings.Session.query(pysql.Comment163).filter(pysql.Comment163.song_id == m[1]).order_by(pysql.Comment163.id).all()
        for c in cms:
            detail = detail + comments.format(c.author,c.liked,c.txt)
        head = title.format(m[1], m[0], m[2], m[3], detail)
        page.append(head + detail)
    body = body.format(uapi.top[playlist_id],"<br>".join(page))

    host,port,users = config.get_mail()
    for user in users.split(","):
        mail.send_email(host,port,"spider163每日网易云音乐分享", user, body)