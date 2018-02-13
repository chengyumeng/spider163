#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import requests

from spider163.utils import encrypt
from spider163.spider import public as uapi
from spider163.utils import pysql
from spider163.utils import pylog
from spider163.utils import tools
from spider163 import settings

class Command():

    def __init__(self):
        modulus = uapi.comment_module
        pubKey = uapi.pubKey
        secKey = uapi.secKey
        self.__encSecKey = self.rsaEncrypt(secKey, pubKey, modulus)
        self.session = requests.session()
        self.session.headers = uapi.header

    def createPlaylistParams(self,ids,playlist_id,cmd,csrf_token):
        text = '{"trackIds":  ['+",".join(ids) + '],"pid": "{}","op": "{}","csrf_token": "{}"'.format(playlist_id,cmd,csrf_token) + '}'
        nonce = '0CoJUm6Qyw8W8jud'
        nonce2 = 16 * 'F'
        encText = encrypt.aes(
            encrypt.aes(text, nonce).decode("utf-8"), nonce2
        )
        return encText

    def createPlaylistRemoveParams(self):
        pass

    def createLoginParams(self,username,password):
        psw = tools.md5(password)
        text = '{' + '"phone": "{}","password": "{}","rememberLogin": "true"'.format(username,psw)+'}'
        nonce = '0CoJUm6Qyw8W8jud'
        nonce2 = 16 * 'F'
        encText = encrypt.aes(
            encrypt.aes(text, nonce).decode("utf-8"), nonce2
        )
        return encText

    def rsaEncrypt(self, text, pubKey, modulus):
        text = text[::-1]
        rs = int(tools.hex(text), 16)**int(pubKey, 16) % int(modulus, 16)
        return format(rs, 'x').zfill(256)

    def createSecretKey(self, size):
        return (
            ''.join(map(lambda xx: (hex(ord(xx))[2:]), os.urandom(size)))
        )[0:16]

    def post_playlist_add(self,ids, playlist_id=2098905487, csrf_token="da2216e4b4ca4efcfab94d8d4920ef9"):
        data = {
            'params': self.createPlaylistParams(ids,playlist_id,"add",csrf_token),
            'encSecKey': self.__encSecKey
        }
        url = uapi.playlist_add_api.format(csrf_token)
        req = self.session.post(
            url, data=data, timeout=10
        )
        return req.json()

    def post_playlist_delete(self, ids, playlist_id=2098905487, csrf_token="da2216e4b4ca4efcfab94d8d4920ef9"):
        data = {
            'params': self.createPlaylistParams(ids, playlist_id, "delete", csrf_token),
            'encSecKey': self.__encSecKey
        }
        url = uapi.playlist_add_api.format(csrf_token)
        req = self.session.post(
            url, data=data, timeout=10
        )
        return req.json()

    def do_login(self,username,password):
        data = {
            'params': self.createLoginParams(username,password),
            'encSecKey': self.__encSecKey
        }
        url = uapi.login_api

        res = self.session.post(url, data=data, timeout=10).json()
        # TODO 处理rep信息
        if res["code"] != 200:
            if res["code"] == 400:
                raise Exception("用户名不合法！")
            raise Exception(res["msg"])
        return res

    def create_playlist_comment_top100(self,playlist_id=2098905487):
        data = settings.Session.query(pysql.Music163.song_name, pysql.Music163.song_id,pysql.Music163.comment.label("count")).order_by(
            pysql.Music163.comment.label("count").desc()).limit(5).all()
        for d in data:
            res = self.post_playlist_add([str(d[1]),],playlist_id)
            if res["code"] == 502:
                pylog.print_warn("歌曲《{}》已经存在于歌单中！".format(d[0]))
            if res["code"] == 200:
                pylog.print_info("成功添加《{}》到指定歌单,歌单目前包含歌曲 {} 首".format(d[0],res["count"]))
        pylog.print_warn("任务完成，请检查！")