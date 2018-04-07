#!/usr/bin/env python
# -*- coding: utf-8 -*-

from spider163 import settings
from spider163 import version
from spider163.utils import pysql
from spider163.utils import mail
from spider163.utils import config


def music(start,stop):
    data = settings.Session.query(
        pysql.Music163.song_name,
        pysql.Music163.song_id,
        pysql.Music163.author,
        pysql.Music163.comment.label("count")
    ).order_by(pysql.Music163.comment.label("count").desc()).slice(start,stop).all()
    page = []
    body = version.MAILBODY
    title = version.MAILMUSIC
    comments = version.MAILCOMMENT
    for m in data:
        detail = ""
        cms = settings.Session.query(pysql.Comment163).filter(pysql.Comment163.song_id == m[1]).order_by(pysql.Comment163.id).all()
        for c in cms:
            detail = detail + comments.format(c.author,c.liked,c.txt)
        head = title.format(m[1], m[0], m[2], m[3],detail)
        page.append(head + detail)
    body = body.format(start,stop,"<br>".join(page))

    host,port,users = config.get_mail()
    for user in users.split(","):
        mail.send_email(host,port,"spider163每日网易云音乐分享", user, body)