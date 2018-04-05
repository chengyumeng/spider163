#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime

from spider163.spider import public as uapi
from spider163 import settings
from spider163.utils import pysql
from spider163.utils import pylog
from spider163.utils import tools
from terminaltables import AsciiTable


class Music:
    
    def __init__(self):
        self.__headers = uapi.header
        self.__url = uapi.music_url
        self.session = settings.Session()

    def views_capture(self,source=None):
        playlist = {}
        if source is None:
            urls = self.session.query(pysql.Playlist163).filter(pysql.Playlist163.done == 'N').order_by(pysql.Playlist163.id).limit(10)
        else:
            if source.startswith("曲风：") is False:
                source = "曲风：" + source
            urls = self.session.query(pysql.Playlist163).filter(pysql.Playlist163.done == 'N',pysql.Playlist163.dsc==source).order_by(pysql.Playlist163.id).limit(1)
        for url in urls:
            print("正在抓取歌单《{}》的歌曲……".format(tools.encode(url.title)))
            songs = self.view_capture(url.link)
            playlist[tools.encode(url.title)] = songs
        return playlist

    def view_capture(self, link):
        url = self.__url + str(link)
        songs = []
        try:
            data = self.curl_playlist(link)
            musics = data['tracks']
            exist = 0
            for music in musics:
                name = tools.encode(music['name'])
                author = tools.encode(music['artists'][0]['name'])
                if music["bMusic"] is None:
                    play_time = 0
                else:
                    play_time = music["bMusic"]["playTime"]
                if pysql.single("music163", "song_id", (music['id'])) is True:
                    self.session.add(pysql.Music163(song_id=music['id'],song_name=name,author=author,playTime=play_time))
                    self.session.commit()
                    exist = exist + 1
                    songs.append({"name": name,"author": author})
                else:
                    pylog.log.info('{} : {} {}'.format("重复抓取歌曲", name, "取消持久化"))
            print("歌单包含歌曲 {} 首,数据库 merge 歌曲 {} 首 \r\n".format(len(musics), exist))
            self.session.query(pysql.Playlist163).filter(pysql.Playlist163.link == link).update({'done': 'Y','update_time': datetime.datetime.now().strftime("%Y-%m-%d %H:%S:%M")})
            self.session.commit()
            return songs
        except Exception as e:
            pylog.log.error("抓取歌单页面存在问题：{} 歌单ID：{}".format(e, url))
            self.session.query(pysql.Playlist163).filter(pysql.Playlist163.link == url).update({'done': 'E', 'update_time': datetime.datetime.now().strftime("%Y-%m-%d %H:%S:%M")})
            self.session.commit()

    def curl_playlist(self,playlist_id):
        url = uapi.playlist_api.format(playlist_id)
        try:
            data = tools.curl(url, self.__headers)
            playlist = data['result']
            self.session.query(pysql.Playlist163).\
                filter(pysql.Playlist163.link == playlist_id).\
                update({"playCount": playlist["playCount"],
                    "shareCount": playlist["shareCount"],
                    "commentCount": playlist["commentCount"],
                    "description": playlist["description"],
                    "tags":",".join(playlist["tags"])})
            return playlist
        except Exception as e:
            pylog.Log("抓取歌单页面存在问题：{} 歌单ID：{}".format(e, playlist_id))
            # pylog.print_warn("抓取歌单页面存在问题：{} 歌单ID：{}".format(e, playlist_id))
            self.session.query(pysql.Playlist163).filter(pysql.Playlist163.link == playlist_id).update({'done': 'E', 'update_time': datetime.datetime.now().strftime("%Y-%m-%d %H:%S:%M")})
            self.session.commit()

    def get_playlist(self, playlist_id):
        self.view_capture(int(playlist_id))
        playlist = self.curl_playlist(playlist_id)

        print("《" + tools.encode(playlist['name']) + "》")
        author = tools.encode(playlist['creator']['nickname'])
        pc = str(playlist['playCount'])
        sc = str(playlist['subscribedCount'])
        rc = str(playlist['shareCount'])
        cc = str(playlist['commentCount'])
        with tools.ignored(Exception):
            print("维护者：{}  播放：{} 关注：{} 分享：{} 评论：{}".format(author, pc, sc, rc, cc))
            print("描述：{}".format(tools.encode(playlist['description'])))
            print("标签：{}".format(",".join(tools.encode(playlist['tags']))))

        tb = [["ID", "歌曲名字", "艺术家", "唱片"]]
        for music in playlist['tracks']:
            artists = []
            for s in music['artists']:
                artists.append(s['name'])
            ms = tools.encode(music['name'])
            ar = tools.encode(",".join(artists))
            ab = tools.encode(music['album']['name'])
            id = music['id']
            tb.append([id, ms, ar, ab])
        print(AsciiTable(tb).table)

    # date
    def create_update_strategy(self, **kwargs):
        date = (datetime.datetime.now() + datetime.timedelta(days=kwargs["date"])).strftime("%Y-%m-%d %H:%S:%M")
        self.session.query(pysql.Music163).filter(pysql.Music163.done=="Y",pysql.Music163.update_time > date).update({ "done": "N","update_time":datetime.datetime.now().strftime("%Y-%m-%d %H:%S:%M")})
        self.session.commit()
        pylog.print_info("完成 重置时间 {} 之后的歌曲，可重新抓取评论".format(date))

