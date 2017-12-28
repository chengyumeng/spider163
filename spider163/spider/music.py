#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import json
from bs4 import BeautifulSoup

import settings as uapi
from spider163 import settings
from spider163.utils import pysql
from spider163.utils import pylog
from terminaltables import AsciiTable


class Music:
    
    def __init__(self):
        self.__headers = uapi.header
        self.__url = uapi.music_url
        self.session = settings.Session()

    def views_capture(self,source=None):
        playlist = {}
        if source is None:
            urls = self.session.query(pysql.Playlist163).filter(pysql.Playlist163.over == 'N').limit(10)
        else:
            if source.startswith("曲风：") is False:
                source = "曲风：" + source
            urls = self.session.query(pysql.Playlist163).filter(pysql.Playlist163.over == 'N',pysql.Playlist163.dsc==source).limit(1)
        for url in urls:
            print("正在抓取歌单《{}》的歌曲……".format(url.title.encode("utf-8")))
            songs = self.view_capture(url.link)
            playlist[url.title.encode("utf-8")] = songs
        for url in urls:
            self.session.query(pysql.Playlist163).filter(pysql.Playlist163.link == url.link).update({'over': 'Y'})
            self.session.commit()
        return playlist

    def view_capture(self, link):
        self.session.query(pysql.Playlist163).filter(pysql.Playlist163.link == link).update({'over': 'Y'})
        url = self.__url + str(link)
        s = requests.session()
        songs = []
        try:
            s = BeautifulSoup(s.get(url, headers=self.__headers).content, "html.parser")
            musics = json.loads(s.text)['result']['tracks']
            exist = 0
            for music in musics:
                name = music['name'].encode('utf-8')
                author = music['artists'][0]['name'].encode('utf-8')
                if pysql.single("music163", "song_id", (music['id'])) is True:
                    self.session.add(pysql.Music163(song_id=music['id'],song_name=name,author=author))
                    self.session.commit()
                    exist = exist + 1
                    songs.append({"name": name,"author": author})
                else:
                    pylog.log.info('{} : {} {}'.format("重复抓取歌曲", name, "取消持久化"))
            print("歌单包含歌曲 {} 首,数据库 merge 歌曲 {} 首 \r\n".format(len(musics), exist))
            return songs
        except Exception as e:
            pylog.log.error("抓取歌单页面存在问题：{} 歌单ID：{}".format(e, url))
            raise

    def get_playlist(self, playlist_id):
        self.view_capture(int(playlist_id))
        url = uapi.playlist_api.format(playlist_id)
        s = requests.session()
        s = BeautifulSoup(s.get(url, headers=self.__headers).content, "html.parser")
        playlist = json.loads(s.text)['result']

        print("《" + playlist['name'].encode('utf-8') + "》")
        author = playlist['creator']['nickname'].encode('utf-8')
        pc = str(playlist['playCount'])
        sc = str(playlist['subscribedCount'])
        rc = str(playlist['shareCount'])
        cc = str(playlist['commentCount'])
        print("维护者：{}  播放：{} 关注：{} 分享：{} 评论：{}".format(author, pc, sc, rc, cc))
        print("描述：{}".format(playlist['description'].encode('utf-8')))
        print("标签：{}".format(",".join(playlist['tags']).encode("utf-8")))

        tb = [["ID", "歌曲名字", "艺术家", "唱片"]]
        for music in playlist['tracks']:
            artists = []
            for s in music['artists']:
                artists.append(s['name'])
            ms = music['name'].encode("utf-8")
            ar = ",".join(artists).encode("utf-8")
            ab = music['album']['name'].encode("utf-8")
            id = music['id']
            tb.append([id, ms, ar, ab])
        print(AsciiTable(tb).table)

