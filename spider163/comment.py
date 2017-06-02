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
        'User-Agent':'android',
        'Cookie': 'appver=1.5.0.75771;',
        'Referer': 'http://music.163.com/'
        }
        text = {
        'username': '13393376853',
        'password': 'wangyidafahao',
        'rememberLogin': 'true'
        }
        modulus = '00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7'
        pubKey  = '010001'
        secKey    = 16 * 'F'
        self.__encSecKey = self.rsaEncrypt(secKey, pubKey, modulus)
    
    def createParams(self,page = 1):
        if page == 1:
            text = '{rid:"", offset:"0", total:"true", limit:"20", csrf_token:""}'
        else :
            offset = str((page-1)*20)
            text = '{rid:"", offset:"%s", total:"%s", limit:"20", csrf_token:""}' %(offset,'false')
        nonce   = '0CoJUm6Qyw8W8jud'
        nonce2  = 16 * 'F'
        encText = self.aesEncrypt(self.aesEncrypt(text,nonce),nonce2)
        return encText

    def aesEncrypt(self, text,secKey):
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

    def viewsCapture(self,song_id,page = 1,pages = 1024):
        if pages > 1:   
            while page < pages:
                pages = self.viewCapture(song_id,page)
                page = page + 1
        else :
            self.viewCapture(song_id,1)

    def viewCapture(self,song_id,page = 1):
        if page == 1:
            dql = "delete from comment163 where song_id = " + str(song_id)
            self.__db.insertSQL(dql)
        data = {'params':self.createParams(page),'encSecKey':self.__encSecKey}
        url  = "http://music.163.com/weapi/v1/resource/comments/R_SO_4_" + str(song_id) + "/?csrf_token="
        # url = "http://music.163.com/eapi/v1/resource/hotcomments/R_SO_4_" + str(song_id)
        try:
           req = requests.post(url,headers = self.__headers ,data = data,timeout = 10)
           for comment in req.json()['comments']:
               if comment['likedCount'] > 30 :
                   sql = "insert into comment163 (song_id,txt,author,liked) values (" + str(song_id) + ",\"" + MySQLdb.escape_string(comment['content'].encode('utf-8')) + "\",\"" + MySQLdb.escape_string(comment['user']['nickname'].encode('utf-8')) + "\"," + str(comment['likedCount']) +")" 
                   self.__db.insertSQL(sql)
           if page == 1 :
               for comment in req.json()['hotComments']:
                   sql = "insert into comment163 (song_id,txt,author,liked) values (" + str(song_id) + ",\"" + MySQLdb.escape_string(comment['content'].encode('utf-8')) + "\",\"" + MySQLdb.escape_string(comment['user']['nickname'].encode('utf-8')) + "\"," + str(comment['likedCount']) +")" 
                   self.__db.insertSQL(sql)
           upd = "update music163 set over ='Y',comment="+ str(req.json()['total'])+ " where song_id = " + str(song_id)
           self.__db.insertSQL(upd)
           return req.json()['total']/20
        except KeyboardInterrupt :
            print("INFO : 解释器请求退出")
        except :
            print("ERROR : SONG_ID-" + str(song_id) + " PAGE-" + str(page))
            self.viewsCapture(song_id,page,page + 1)



# if __name__ == "__main__":
#     tmp = Comment()
#     tmp.viewsCapture(28793140,1,2)
#     tmp.viewsCapture(28793142,1,2)
