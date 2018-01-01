#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import os
import base64
import json

from Crypto.Cipher import AES
from bs4 import BeautifulSoup
from terminaltables import AsciiTable


import settings as uapi
from spider163 import settings
from spider163.utils import pysql
from spider163.utils import pylog

class MP3:

    def __init__(self):
        self.__headers = uapi.header
        self.session = settings.Session()
        text = uapi.comment_text
        modulus = uapi.comment_module
        pubKey = uapi.pubKey
        secKey = uapi.secKey
        self.__encSecKey = self.rsa_encrypt(secKey, pubKey, modulus)

    def create_params(self, song_id):
        text = '{"ids":['+ str(song_id) + '], br:"320000",csrf_token:"csrf"}'
        nonce = '0CoJUm6Qyw8W8jud'
        nonce2 = 16 * 'F'
        encText = self.aes_encrypt(self.aes_encrypt(text,nonce),nonce2)
        return encText

    def aes_encrypt(self, text, secKey):
        pad = 16 - len(text) % 16
        text = text + pad * chr(pad)
        encryptor = AES.new(secKey, 2, '0102030405060708')
        ciphertext = encryptor.encrypt(text)
        ciphertext = base64.b64encode(ciphertext)
        return ciphertext

    def rsa_encrypt(self, text, pubKey, modulus):
        text = text[::-1]
        rs = int(text.encode('hex'), 16)**int(pubKey, 16) % int(modulus, 16)
        return format(rs, 'x').zfill(256)

    def create_secretKey(self, size):
        return (''.join(map(lambda xx: (hex(ord(xx))[2:]), os.urandom(size))))[0:16]

    def view_down(self, playlist_id, path="."):
        list = self.get_playlist(playlist_id)
        for music in list['tracks']:
            pylog.print_info(
                "正在下载歌曲 {}-{}.mp3".format(music['name'].encode("utf-8"), music['artists'][0]['name'].encode("utf-8")))
            link = self.get_mp3_link(music["id"])
            r = requests.get(link)
            with open("{}/{}-{}{}".format(path, music['name'].encode("utf-8").replace("/","-"), music['artists'][0]['name'].encode("utf-8").replace("/","-"), ".mp3"), "wb") as code:
                code.write(r.content)

    def get_playlist(self, playlist_id):
        url = uapi.playlist_api.format(playlist_id)
        try:
            s = requests.session()
            s = BeautifulSoup(s.get(url, headers=self.__headers).content, "html.parser")
            playlist = json.loads(s.text)['result']
            return playlist
        except Exception as e:
            raise

    def get_mp3_link(self, song_id):
        data = {'params': self.create_params(song_id), 'encSecKey': self.__encSecKey}
        url = uapi.mp3_url
        try:
            req = requests.post(url, headers=self.__headers, data=data, timeout=10).json()
            if req['code'] == 200:
                return req['data'][0]['url']
        except Exception as e:
            raise