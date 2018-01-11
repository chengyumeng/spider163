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
play_url = "http://music.163.com/discover/playlist/?order=hot&cat={}&limit=35&offset={}"
music_url = "http://music.163.com/api/playlist/detail?id="
mp3_url = "http://music.163.com/weapi/song/enhance/player/url?csrf_token="

playlist_api = "http://music.163.com/api/playlist/detail?id={}&upd"

music_api = "http://music.163.com/api/song/detail/?id={}&ids=[{}]"

search_api = "http://music.163.com/api/search/pc"

classify = {
    "语种":["华语", "欧美", "日语","韩语", "粤语", "小语种", ],
    "风格":["流行", "摇滚", "民谣", "电子", "舞曲", "说唱", "轻音乐", "爵士", "乡村", "R&B/Soul", "古典", "民族", "英伦", "金属", "朋克", "蓝调", "雷鬼", "世界音乐", "拉丁", "另类/独立", "New Age", "古风", "后摇", "Bossa Nova"],
    "场景":["清晨", "夜晚", "学习", "工作", "午休", "下午茶", "地铁", "驾车", "运动", "旅行", "散步", "酒吧"],
    "情感":["怀旧", "清新", "浪漫", "性感", "伤感", "治愈", "放松", "孤独", "感动", "兴奋", "快乐", "安静", "思念"],
    "主题":["影视原声", "ACG", "校园", "游戏", "70后", "80后", "90后", "网络歌曲", "KTV", "经典", "翻唱", "吉他", "钢琴", "器乐", "儿童", "榜单", "00后"]
}
