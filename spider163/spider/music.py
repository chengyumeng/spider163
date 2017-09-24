#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import json
from bs4 import BeautifulSoup

import default
from spider163 import settings
from spider163.utils import pysql
from spider163.utils import pylog


class Music:
    
    def __init__(self):
        self.__headers = default.header
        self.__url = default.music_url
        self.session = settings.Session()

    def views_capture(self):
        urls = self.session.query(pysql.Playlist163).filter(pysql.Playlist163.over == 'N').limit(10)
        for url in urls:
            self.view_capture(url.link)
        for url in urls:
            self.session.query(pysql.Playlist163).filter(pysql.Playlist163.link == url.link).update({'over': 'Y'})
            self.session.commit()
        return urls.count()

    def view_capture(self, link):
        self.session.query(pysql.Playlist163).filter(pysql.Playlist163.link == link).update({'over': 'Y'})
        url = self.__url + str(link)
        s = requests.session()
        try:
            s = BeautifulSoup(s.get(url, headers=self.__headers).content, "html.parser")
            musics = json.loads(s.text)['result']['tracks']
            for music in musics:
                name = music['name'].encode('utf-8')
                author = music['artists'][0]['name'].encode('utf-8')
                if pysql.single("music163", "song_id", (music['id'])) == True:
                    self.session.add(pysql.Music163(song_id=music['id'],song_name=name,author=author))
                    self.session.commit()
                else:
                    pylog.Log('{} : {} {}'.format("ERROR 103",name,"Not Single"))
        except:
            pylog.Log('{} : {}'.format("Error 901", url))


if __name__ == "__main__":
    tmp = Music()
    print tmp.views_capture()
