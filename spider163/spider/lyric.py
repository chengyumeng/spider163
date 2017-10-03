#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import json
from bs4 import BeautifulSoup

import default
from spider163 import settings
from spider163.utils import pysql
from spider163.utils import pylog


class Lyric:

    def __init__(self):
        self.__headers = default.header
        self.session = settings.Session()

    def view_lyric(self, song_id):
        url = default.lyric_url.format(str(song_id))
        s = requests.session()
        try:
            s = BeautifulSoup(s.get(url, headers=self.__headers).content, "html.parser")
            lrc = json.loads(s.text)['lrc']['lyric']
            if pysql.single("lyric163", "song_id", song_id):
                self.session.add(pysql.Lyric163(song_id=song_id, txt=lrc))
                self.session.query(pysql.Music163).filter(pysql.Music163.song_id == song_id).update({"has_lyric": "Y"})
                self.session.commit()
        except Exception:
            pylog.log.error("抓取歌词出现问题，歌曲ID：" + str(song_id))
            raise

    def get_lyric(self, song_id):
        self.view_lyric(song_id)
        lrc = self.session.query(pysql.Lyric163).filter(pysql.Lyric163.song_id == song_id)
        print(lrc[0].txt)

    def view_lyrics(self, count):
        for i in range(count/10):
            ms = self.session.query(pysql.Music163).filter(pysql.Music163.has_lyric == "N").limit(10)
            for m in ms:
                print("歌曲ID " + str(m.song_id))
                self.view_lyric(m.song_id)
        ms = self.session.query(pysql.Music163).filter(pysql.Music163.has_lyric == "N").limit(count%10)
        for m in ms:
            self.view_lyric(m.song_id)


if __name__ == "__main__":
    # tmp = Lyric()
    # tmp.view_lyric(506092019)
    Lyric().view_lyrics(19)