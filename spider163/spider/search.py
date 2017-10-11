#!/usr/bin/env python
# -*- coding: utf-8 -*-

import default
import requests
from terminaltables import AsciiTable
from spider163.utils import pylog

offset = 0
limit = 20
type = {1: "歌曲", 10: "专辑", 100: "歌手", 1000: "歌单"}


def searchSong(key):
    url = default.search_api
    data = {'s': key, 'offset': 0, 'limit': 20, 'type': "1"}
    req = requests.post(url, headers=default.header, data=data, timeout=10)
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
    url = default.search_api
    data = {'s': key, 'offset': 0, 'limit': 20, 'type': "10"}
    req = requests.post(url, headers=default.header, data=data, timeout=10)
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



if __name__ == "__main__":
    searchSong("林依晨")