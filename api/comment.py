#!/usr/bin/env python
# -*- coding: utf-8 -*-


import requests
import json
import os
import base64
from Crypto.Cipher import AES
from pprint import pprint
import MySQLdb
import sys
import ConfigParser
import db

class Comment:
    
    def __init__(self):
        self.__db = db.MySQLDB()
        self.__headers = {
        'Cookie': 'appver=1.5.0.75771;',
        'Referer': 'http://music.163.com/'
        }
        text = {
        'username': '13393376853',
        'password': 'wangyidafahao',
        'rememberLogin': 'true'
        }
        modulus = '00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7'
        nonce   = '0CoJUm6Qyw8W8jud'
        pubKey  = '010001'
        secKey    = self.createSecretKey(16)
        encText   = self.aesEncrypt(self.aesEncrypt(json.dumps(text), nonce), secKey)
        encSecKey = self.rsaEncrypt(secKey, pubKey, modulus)
        self.__data = data = {
            'params': encText,
            'encSecKey': encSecKey
        }

    def aesEncrypt(self,text, secKey):
        pad = 16 - len(text) % 16
        text = text + pad * chr(pad)
        encryptor = AES.new(secKey, 2, '0102030405060708')
        ciphertext = encryptor.encrypt(text)
        ciphertext = base64.b64encode(ciphertext)
        return ciphertext

    def rsaEncrypt(self,text, pubKey, modulus):
        text = text[::-1]
        rs = int(text.encode('hex'), 16)**int(pubKey, 16) % int(modulus, 16)
        return format(rs, 'x').zfill(256)

    def createSecretKey(self,size):
        return (''.join(map(lambda xx: (hex(ord(xx))[2:]), os.urandom(size))))[0:16]

    def viewCapture(self,song_id):
        url = "http://music.163.com/weapi/v1/resource/comments/R_SO_4_" + str(song_id) + "/?csrf_token="
        try:
           req = requests.post(url,headers = self.__headers ,data = self.__data)
           for comment in req.json()['comments']:
               sql = "insert into comment163 (song_id,txt,author,liked) values (" + str(song_id) + ",'" + MySQLdb.escape_string(comment['content'].encode('utf-8')) + "','" + MySQLdb.escape_string(comment['user']['nickname'].encode('utf-8')) + "'," + str(comment['likedCount']) +")" 
               self.__db.insertSQL(sql)
           for comment in req.json()['hotComments']:
               sql = "insert into comment163 (song_id,txt,author,liked) values (" + str(song_id) + ",'" + MySQLdb.escape_string(comment['content'].encode('utf-8')) + "','" + MySQLdb.escape_string(comment['user']['nickname'].encode('utf-8')) + "'," + str(comment['likedCount']) +")" 
               self.__db.insertSQL(sql)
        except:
            pprint(requests.post(url,headers = self.__headers ,data = self.__data).json())
            print("ERROR " + str(song_id))


if __name__ == "__main__":
    tmp = Comment()
    tmp.viewCapture(28793140)

