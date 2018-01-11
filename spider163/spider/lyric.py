#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import json

from bs4 import BeautifulSoup

import settings as uapi
from spider163 import settings
from spider163.utils import pysql
from spider163.utils import pylog


class Lyric:

    def __init__(self):
        self.__headers = uapi.header
        self.session = settings.Session()

    def view_lyric(self, song_id):
        url = uapi.lyric_url.format(str(song_id))
        s = requests.session()
        try:
            s = BeautifulSoup(s.get(url, headers=self.__headers).content, "html.parser")
            lrc = json.loads(s.text)['lrc']['lyric']
            if pysql.single("lyric163", "song_id", song_id):
                self.session.add(pysql.Lyric163(song_id=song_id, txt=lrc))
                self.session.query(pysql.Music163).filter(pysql.Music163.song_id == song_id).update({"has_lyric": "Y"})
                self.session.commit()
        except Exception as e:
            self.session.query(pysql.Music163).filter(pysql.Music163.song_id == song_id).update({"has_lyric": "E"})
            self.session.commit()
            pylog.log.error("抓取歌词出现问题：{} 歌曲ID：{}".format(e, song_id))
            # raise

    def get_lyric(self, song_id):
        self.view_lyric(song_id)
        lrc = self.session.query(pysql.Lyric163).filter(pysql.Lyric163.song_id == song_id)
        print(lrc[0].txt)

    def view_lyrics(self, count):
        song = []
        for i in range(count/10):
            ms = self.session.query(pysql.Music163).filter(pysql.Music163.has_lyric == "N").limit(10)
            for m in ms:
                print("正在抓取歌词 ID {} 歌曲 {}".format(m.song_id, pylog.Blue(m.song_name.encode("utf-8"))))
                self.view_lyric(m.song_id)
                song.append({"name": m.song_name,"author": m.author,"comment": m.comment})
        ms = self.session.query(pysql.Music163).filter(pysql.Music163.has_lyric == "N").limit(count%10)
        for m in ms:
            print("正在抓取歌词 ID {} 歌曲 {}".format(m.song_id, pylog.Blue(m.song_name.encode("utf-8"))))
            self.view_lyric(m.song_id)
            song.append({"name": m.song_name, "author": m.author, "comment": m.comment})
        return song
