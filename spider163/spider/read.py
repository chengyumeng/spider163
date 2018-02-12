#!/usr/bin/env python
# -*- coding: utf-8 -*-

from docx import Document
from docx.shared import Inches

from spider163.spider import public as uapi
from spider163.utils import tools
from spider163.utils import pylog
from spider163.spider import comment


def read_playlist_json(id):
    url = uapi.playlist_api.format(id)
    data = tools.curl(url,uapi.header)
    return data


def read_music_data(id):
    url = uapi.mp3_url.format(id)


def read_comment_data(id):
    cmt = comment.Comment()
    return cmt.post(id,1)


def read_lyric_data(id):
    url = uapi.lyric_url.format(id)
    data = tools.curl(url,uapi.header)
    return data


def print_pdf(id):
    data = read_playlist_json(id)
    if data["code"] != 200:
        pylog.print_warn("歌单信息拉取失败！")
        return

    document = Document()
    try:
        document.add_heading(data["result"]["name"], 0)
        desc = document.add_paragraph(data["result"]["description"])
        tags = document.add_paragraph(" ".join(data["result"]["tags"]))
        for m in data["result"]["tracks"]:
            p = document.add_paragraph()
            p.add_run(m["name"])

            lyric = read_lyric_data(m["id"])
            document.add_paragraph(lyric["lrc"]["lyric"])

            comments = read_comment_data(m["id"])
            for c in comments["hotComments"]:
                content = document.add_paragraph(c["content"])
                # liked = document.add_paragraph(c["likedCount"])
                author = document.add_paragraph(c["user"]["nickname"])
    except Exception as e:
        print(e)

    document.save('demo.docx')