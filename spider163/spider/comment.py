#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import requests

from bs4 import BeautifulSoup
from terminaltables import AsciiTable

from spider163 import settings
from spider163.utils import pysql
from spider163.utils import pylog
from spider163.utils import tools
from spider163.utils import encrypt
from spider163.spider import public as uapi


class Comment:

    def __init__(self):
        self.__headers = uapi.header
        self.session = settings.Session()
        modulus = uapi.comment_module
        pubKey = uapi.pubKey
        secKey = uapi.secKey
        self.__encSecKey = self.rsaEncrypt(secKey, pubKey, modulus)

    def createParams(self, page=1):
        if page == 1:
            text = (
                '{rid:"", offset:"0", total:"true", limit:"20", csrf_token:""}'
            )
        else:
            offset = str((page-1)*20)
            text = (
                '{rid:"", offset:"{}", total:"{}", limit:"20", '
                'csrf_token:""}'.format(offset, 'false')
            )
        nonce = '0CoJUm6Qyw8W8jud'
        nonce2 = 16 * 'F'
        encText = encrypt.aes(
            encrypt.aes(text, nonce).decode("utf-8"), nonce2
        )
        return encText

    def rsaEncrypt(self, text, pubKey, modulus):
        text = text[::-1]
        rs = int(tools.hex(text), 16)**int(pubKey, 16) % int(modulus, 16)
        return format(rs, 'x').zfill(256)

    def createSecretKey(self, size):
        return (
            ''.join(map(lambda xx: (hex(ord(xx))[2:]), os.urandom(size)))
        )[0:16]

    def post(self,song_id,page):
        data = {
            'params': self.createParams(page),
            'encSecKey': self.__encSecKey
        }
        url = uapi.comment_url.format(song_id)
        req = requests.post(
            url, headers=self.__headers, data=data, timeout=10
        )
        return req.json()

    def views_capture(self, song_id, page=1, pages=1024):
        if pages > 1:
            while page < pages:
                pages = self.view_capture(song_id, page)
                page = page + 1
        else:
            self.view_capture(song_id, 1)
        self.view_links(song_id)


    def view_capture(self, song_id, page=1):
        if page == 1:
            self.session.query(pysql.Comment163).filter(
                pysql.Comment163.song_id == song_id
            ).delete()
            self.session.commit()
        try:
            data = self.post(song_id,page)
            for comment in data['comments']:
                if comment['likedCount'] > 30:
                    txt = tools.encode(comment['content'])
                    author = tools.encode(comment['user']['nickname'])
                    liked = comment['likedCount']
                    self.session.add(pysql.Comment163(
                        song_id=song_id, txt=txt, author=author, liked=liked
                    ))
                    self.session.flush()
            if page == 1:
                for comment in data['hotComments']:
                    txt = tools.encode(comment['content'])
                    author = tools.encode(comment['user']['nickname'])
                    liked = comment['likedCount']
                    self.session.add(pysql.Comment163(
                        song_id=song_id, txt=txt, author=author, liked=liked
                    ))
                    self.session.flush()
            cnt = int(data['total'])
            self.session.query(pysql.Music163).filter(
                pysql.Music163.song_id == song_id
            ).update({'over': 'Y', 'comment': cnt})
            self.session.commit()
            return cnt / 20
        except Exception as e:
            self.session.rollback()
            self.session.query(pysql.Music163).filter(
                pysql.Music163.song_id == song_id
            ).update({'over': 'Y', 'comment': -2})
            self.session.commit()
            pylog.log.error(
                "解析歌曲评论的时候出现问题:{} 歌曲ID：{} 页码：{}".format(
                    e, song_id, page
                )
            )
            raise

    def view_links(self, song_id):
        url = "http://music.163.com/song?id=" + str(song_id)
        data = {'id': str(song_id)}
        headers = {
            'Cookie': 'MUSIC_U=e45797021db3403ab9fffb11c0f70a7994f71177b26efb5169b46948f2f9a60073d23a2665346106c9295f8f6dbb6c7731b299d667364ed3;'  # noqa
        }
        try:
            req = requests.get(url, headers=headers, data=data, timeout=100)
            sup = BeautifulSoup(req.content, "html.parser")
            for link in sup.find_all('li', class_="f-cb"):
                html = link.find('a', 's-fc1')
                if html is not None:
                    title = tools.encode(html.get('title'))
                    song_id = html.get('href')[9:]
                    author = tools.encode(link.find(
                        'div', 'f-thide s-fc4'
                    ).find('span').get('title'))
                    if pysql.single("music163", "song_id", song_id) is True:
                        self.session.add(pysql.Music163(
                            song_id=song_id, song_name=title, author=author
                        ))
                        self.session.flush()
            for link in sup.find_all('a', 'sname f-fs1 s-fc0'):
                play_link = link.get("href").replace("/playlist?id=", "")
                play_name = tools.encode(link.get("title"))
                if pysql.single("playlist163", "link", play_link) is True:
                    self.session.add(pysql.Playlist163(
                        title=play_name, link=play_link, cnt=-1,
                        dsc="来源：热评"
                    ))
                    self.session.flush()
        except Exception as e:
            pylog.log.error("解析页面推荐时出现问题：{} 歌曲ID：{}".format(e, song_id))

    def auto_view(self, count=1):
        song = []
        if count < 10:
            msc = self.session.query(pysql.Music163).filter(
                pysql.Music163.over == "N"
            ).limit(count)
            for m in msc:
                try:
                    print(
                        "抓取热评 ID {} 歌曲 {}".format(
                            m.song_id, pylog.Blue(tools.encode(m.song_name))
                        )
                    )
                    self.views_capture(m.song_id, 1, 1)
                    song.append({
                        "name": m.song_name, "author": m.author,
                        "song_id": m.song_id
                    })
                except Exception as e:
                    self.session.rollback()
                    pylog.log.error(
                        "自动抓取热评出现异常：{} 歌曲ID：{}".format(e, m.song_id)
                    )
        else:
            for i in range(int(count / 10)):
                msc = self.session.query(pysql.Music163).filter(
                    pysql.Music163.over == "N"
                ).limit(10)
                for m in msc:
                    try:
                        print(
                            "抓取热评 ID {} 歌曲 {}".format(
                                m.song_id,
                                pylog.Blue(tools.encode(m.song_name))
                            )
                        )
                        self.views_capture(m.song_id, 1, 1)
                        song.append({
                            "name": m.song_name, "author": m.author,
                            "song_id": m.song_id
                        })
                    except Exception as e:
                        self.session.rollback()
                        pylog.log.error(
                            "自动抓取热评出现异常：{} 歌曲ID：{}".format(
                                e, m.song_id
                            )
                        )
            msc = self.session.query(pysql.Music163).filter(
                pysql.Music163.over == "N"
            ).limit(count % 10)
            for m in msc:
                try:
                    print(
                        "抓取热评 ID {} 歌曲 {}".format(
                            m.song_id, pylog.Blue(tools.encode(m.song_name))
                        )
                    )
                    self.views_capture(m.song_id, 1, 1)
                    song.append({
                        "name": m.song_name, "author": m.author,
                        "song_id": m.song_id
                    })
                except Exception as e:
                    self.session.rollback()
                    pylog.log.error(
                        "自动抓取热评出现异常：{} 歌曲ID：{}".format(e, m.song_id)
                    )

        return song

    def get_music(self, music_id):
        self.view_capture(int(music_id), 1)
        url = uapi.music_api.format(music_id, music_id)
        data = tools.curl(url,self.__headers)
        music = data['songs']
        print("《" + tools.encode(music[0]['name']) + "》")
        author = []
        for a in music[0]['artists']:
            author.append(tools.encode(a['name']))
        album = str(tools.encode(music[0]['album']['name']))
        print("演唱：{}     专辑：{}".format("，".join(author), album))
        comments = self.session.query(pysql.Comment163).filter(
            pysql.Comment163.song_id == int(music_id)
        )
        tb = AsciiTable([["序号", "作者", "评论", "点赞"]])
        max_width = tb.column_max_width(2) - tb.column_max_width(2) % 3
        cnt = 0
        try:
            for cmt in comments:
                cnt = cnt + 1
                au = tools.encode(cmt.author)
                txt = ""
                length = 0
                for u in cmt.txt:
                    txt = txt + u
                    if ord(u) < 128:
                        length = length + 3
                    else:
                        length = length + 1
                    if length == max_width:
                        txt = txt + "\n"
                        length = 0
                liked = str(cmt.liked)
                tb.table_data.append([str(cnt), str(au), str(txt), liked])
            print(tb.table)
        except UnicodeEncodeError:
            pylog.log.info("获取歌曲详情编码存在问题，转为非表格形式，歌曲ID：{}".format(music_id))
            for cmt in comments:
                print("评论： {}".format(tools.encode(cmt.txt)))
                print(
                    "作者： {}   点赞：  {}".format(
                        tools.encode(cmt.author), str(cmt.liked)
                    )
                )
                print("")
        except Exception as e:
            pylog.print_warn("获取歌曲时出现异常： {} 歌曲ID：{}".format(e, music_id))
