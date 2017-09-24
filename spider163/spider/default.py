#!/usr/bin/env python
# -*- coding: utf-8 -*-

header = {
            'Referer': 'http://music.163.com/',
            'Host': 'music.163.com',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
        }
comment_text = {
        'username': '13393376853',
        'password': 'wangyidafahao',
        'rememberLogin': 'true'
        }
comment_module = '00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7'
pubKey = '010001'
secKey = 16 * 'F'
comment_url = "http://music.163.com/weapi/v1/resource/comments/R_SO_4_{}/?csrf_token="
lyric_url = "http://music.163.com/api/song/lyric?os=pc&id={}&lv=-1&kv=-1&tv=-1"
play_url = "http://music.163.com/discover/playlist/?order=hot&cat=全部&limit=35&offset="
music_url = "http://music.163.com/api/playlist/detail?id="