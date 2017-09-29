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
                self.session.commit()
        except:
            pylog.Log("抓取歌词出现问题，歌曲ID：" + str(song_id))

    def get_lyric(self, song_id):
        self.view_lyric(song_id)
        lrc = self.session.query(pysql.Lyric163).filter(pysql.Lyric163.song_id == song_id)
        print(lrc[0].txt)


if __name__ == "__main__":
    tmp = Lyric()
    tmp.view_lyric(506092019)