#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import json
import requests

from bs4 import BeautifulSoup
from terminaltables import AsciiTable

from spider163 import settings
from spider163.utils import pylog
from spider163.utils import tools
from spider163.utils import encrypt
from spider163.spider import public as uapi


class MP3:

    def __init__(self):
        self.__headers = uapi.header
        self.session = settings.Session()
        modulus = uapi.comment_module
        pubKey = uapi.pubKey
        secKey = uapi.secKey
        self.__encSecKey = self.rsa_encrypt(secKey, pubKey, modulus)

    def create_params(self, song_id):
        text = '{"ids":[' + str(song_id) + '], br:"320000",csrf_token:"csrf"}'
        nonce = '0CoJUm6Qyw8W8jud'
        nonce2 = 16 * 'F'
        encText = encrypt.aes(
            encrypt.aes(text, nonce).decode("utf-8"), nonce2
        )
        return encText

    def rsa_encrypt(self, text, pubKey, modulus):
        text = text[::-1]
        rs = int(tools.hex(text), 16)**int(pubKey, 16) % int(modulus, 16)
        return format(rs, 'x').zfill(256)

    def create_secretKey(self, size):
        return (
            ''.join(map(lambda xx: (hex(ord(xx))[2:]), os.urandom(size)))
        )[0:16]

    def view_down(self, playlist_id, path="."):
        list = self.get_playlist(playlist_id)
        msg = {"success": 0, "failed": 0, "failed_list": []}
        for music in list['tracks']:
            pylog.print_info(
                "正在下载歌曲 {}-{}.mp3".format(
                    tools.encode(music['name']),
                    tools.encode(music['artists'][0]['name'])
                )
            )
            link = self.get_mp3_link(music["id"])
            if link is None:
                msg["failed"] = msg["failed"] + 1
                msg["failed_list"].append(music)
                continue
            r = requests.get(link)
            with open("{}/{}-{}{}".format(
                path,
                tools.encode(music['name']).replace("/", "-"),
                tools.encode(music['artists'][0]['name']).replace("/", "-"),
                ".mp3"
            ), "wb") as code:
                code.write(r.content)
                msg["success"] = msg["success"] + 1
        pylog.print_warn(
            "下载成功：{} 首，下载失败：{}首".format(msg["success"], msg["failed"])
        )
        tb = [["歌曲名字", "艺术家", "ID"]]
        for music in msg["failed_list"]:
            n = music['name'].encode("utf-8")
            a = music['artists'][0]['name'].encode("utf-8")
            i = music['id']
            tb.append([n, a, i])
        print(AsciiTable(tb).table)

    def get_playlist(self, playlist_id):
        url = uapi.playlist_api.format(playlist_id)
        try:
            s = requests.session()
            s = BeautifulSoup(
                s.get(url, headers=self.__headers).content, "html.parser"
            )
            playlist = json.loads(s.text)['result']
            return playlist
        except Exception as e:
            raise

    def get_mp3_link(self, song_id):
        data = {
            'params': self.create_params(song_id),
            'encSecKey': self.__encSecKey
        }
        url = uapi.mp3_url
        try:
            req = requests.post(
                url, headers=self.__headers, data=data, timeout=10
            ).json()
            if req['code'] == 200:
                return req['data'][0]['url']
        except Exception as e:
            raise
