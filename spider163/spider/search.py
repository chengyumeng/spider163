#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
from terminaltables import AsciiTable

from spider163.utils import pylog
import settings as uapi

offset = 0
limit = 20
type = {1: "歌曲", 10: "专辑", 100: "歌手", 1000: "歌单"}


def searchSong(key):
    url = uapi.search_api
    data = {'s': key, 'offset': 0, 'limit': 20, 'type': "1"}
    req = requests.post(url, headers=uapi.header, data=data, timeout=10)
    if req.json()["result"]['songCount'] == 0:
        pylog.log.warn("关键词 {} 没有可搜索歌曲".format(key))
        return
    songs = req.json()["result"]['songs']
    song_table = AsciiTable([["ID", "歌曲", "专辑", "演唱"]])
    for item in songs:
        id = item['id']
        name = (item['name']).encode("utf-8")
        album = (item['album']['name']).encode("utf-8")
        artist = []
        for a in item['artists']:
            artist.append(a['name'].encode("utf-8"))
        song_table.table_data.append([str(id), name, album, ",".join(artist)])
    print(pylog.Blue("与 \"{}\" 有关的歌曲".format(key)))
    print(song_table.table)


def searchAlbum(key):
    url = uapi.search_api
    data = {'s': key, 'offset': 0, 'limit': 20, 'type': "10"}
    req = requests.post(url, headers=uapi.header, data=data, timeout=10)
    if req.json()["result"]['albumCount'] == 0:
        pylog.log.warn("关键词 {} 没有可搜索专辑".format(key))
        return
    albums = req.json()["result"]['albums']
    song_table = AsciiTable([["ID", "专辑", "演唱","发行方"]])
    for item in albums:
        id = item['id']
        name = item['name'].encode("utf-8")
        company = ""
        if item['company'] !=  None:
            company = item['company'].encode("utf-8")
        artist = []
        for a in item['artists']:
            artist.append(a['name'].encode("utf-8"))
        song_table.table_data.append([str(id), name, ",".join(artist), company])
    print(pylog.Blue("与 \"{}\" 有关的专辑".format(key)))
    print(song_table.table)


def searchSinger(key):
    url = uapi.search_api
    data = {'s': key, 'offset': 0, 'limit': 10, 'type': "100"}
    req = requests.post(url, headers=uapi.header, data=data, timeout=10)
    if req.json()["result"]['artistCount'] == 0:
        pylog.log.warn("关键词 {} 没有可搜索艺术家".format(key))
        return
    artists = req.json()["result"]['artists']
    song_table = AsciiTable([["ID", "姓名", "专辑数量", "MV数量"]])
    for item in artists:
        id = str(item['id'])
        name = item['name'].encode("utf-8")
        acount = str(item['albumSize'])
        mcount = str(item['mvSize'])
        song_table.table_data.append([id, name, acount, mcount])
    print(pylog.Blue("与 \"{}\" 有关的歌手".format(key)))
    print(song_table.table)


def searchPlaylist(key):
    url = uapi.search_api
    data = {'s': key, 'offset': 0, 'limit': 5, 'type': "1000"}
    req = requests.post(url, headers=uapi.header, data=data, timeout=10)
    if req.json()["result"]['playlistCount'] == 0:
        pylog.log.warn("关键词 {} 没有可搜索歌单".format(key))
        return
    playlists = req.json()["result"]['playlists']
    song_table = AsciiTable([["ID", "歌单", "维护者", "播放数量", "收藏数量"]])
    for item in playlists:
        id = str(item['id'])
        name = item['name'].encode("utf-8")
        creator = item['creator']['nickname'].encode("utf-8")
        pcount = str(item['playCount'])
        bcount = str(item['bookCount'])
        song_table.table_data.append([id, name, creator, pcount, bcount])
    print(pylog.Blue("与 \"{}\" 有关的歌单".format(key)))
    print(song_table.table)