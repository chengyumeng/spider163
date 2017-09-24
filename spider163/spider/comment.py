#!/usr/bin/env python
# -*- coding: utf-8 -*-


import requests
import os
import base64
from Crypto.Cipher import AES
from bs4 import BeautifulSoup

import default
from spider163 import settings
from spider163.utils import pysql
from spider163.utils import pylog


class Comment:

    def __init__(self):
        self.__headers = default.header
        self.session = settings.Session()
        text = default.comment_text
        modulus = default.comment_module
        pubKey = default.pubKey
        secKey = default.secKey
        self.__encSecKey = self.rsaEncrypt(secKey, pubKey, modulus)

    def createParams(self, page=1):
        if page == 1:
            text = '{rid:"", offset:"0", total:"true", limit:"20", csrf_token:""}'
        else:
            offset = str((page-1)*20)
            text = '{rid:"", offset:"%s", total:"%s", limit:"20", csrf_token:""}' %(offset,'false')
        nonce = '0CoJUm6Qyw8W8jud'
        nonce2 = 16 * 'F'
        encText = self.aesEncrypt(self.aesEncrypt(text,nonce),nonce2)
        return encText

    def aesEncrypt(self, text, secKey):
        pad = 16 - len(text) % 16
        text = text + pad * chr(pad)
        encryptor = AES.new(secKey, 2, '0102030405060708')
        ciphertext = encryptor.encrypt(text)
        ciphertext = base64.b64encode(ciphertext)
        return ciphertext

    def rsaEncrypt(self, text, pubKey, modulus):
        text = text[::-1]
        rs = int(text.encode('hex'), 16)**int(pubKey, 16) % int(modulus, 16)
        return format(rs, 'x').zfill(256)

    def createSecretKey(self, size):
        return (''.join(map(lambda xx: (hex(ord(xx))[2:]), os.urandom(size))))[0:16]

    def views_capture(self, song_id, page=1, pages=1024):
        if pages > 1:   
            while page < pages:
                pages = self.view_capture(song_id, page)
                page = page + 1
        else:
            self.view_capture(song_id, 1)
        self.view_links(song_id)
    
    def view_capture(self, song_id, page=1):
        if page == 1:
            self.session.query(pysql.Comment163).filter(pysql.Comment163.song_id == song_id).delete()
            self.session.commit()
        data = {'params': self.createParams(page), 'encSecKey': self.__encSecKey}
        url = default.comment_url.format(str(song_id))
        try:
            req = requests.post(url, headers=self.__headers, data=data, timeout=10)
            for comment in req.json()['comments']:
                if comment['likedCount'] > 30:
                    txt = comment['content'].encode('utf-8')
                    author = comment['user']['nickname'].encode('utf-8')
                    liked = comment['likedCount']
                    self.session.add(pysql.Comment163(song_id=song_id, txt=txt, author=author, liked=liked))
                    self.session.commit()
            if page == 1:
                for comment in req.json()['hotComments']:
                    txt = comment['content'].encode('utf-8')
                    author = comment['user']['nickname'].encode('utf-8')
                    liked = comment['likedCount']
                    self.session.add(pysql.Comment163(song_id=song_id, txt=txt, author=author, liked=liked))
                    self.session.commit()
            cnt = int(req.json()['total'])
            self.session.query(pysql.Music163).filter(pysql.Music163.song_id == song_id).update({'over': 'Y', 'comment': cnt})
            self.session.commit()
            return cnt / 20
        except KeyboardInterrupt:
            print("INFO : 解释器请求退出")
            pylog.Log("ERROR 107 : 解释器请求退出")
            exit()
        except:
            pylog.Log("ERROR 910 : SONG_ID-" + str(song_id) + " PAGE-" + str(page))

    def view_links(self, song_id):
        url = "http://music.163.com/song?id=" + str(song_id)
        data = {'id': str(song_id)}
        headers = {'Cookie': 'MUSIC_U=e45797021db3403ab9fffb11c0f70a7994f71177b26efb5169b46948f2f9a60073d23a2665346106c9295f8f6dbb6c7731b299d667364ed3;'}
        req = requests.get(url, headers=headers, data=data, timeout=100)
        sup = BeautifulSoup(req.content, "html.parser")
        for link in sup.find_all('li', class_="f-cb"):
            html = link.find('a', 's-fc1')
            if html != None:
                title = html.get('title').encode('utf-8')
                song_id = html.get('href')[9:]
                author = link.find('div', 'f-thide s-fc4').find('span').get('title').encode('utf-8')
                if pysql.single("music163","song_id",song_id) == True:
                    self.session.add(pysql.Music163(song_id=song_id, song_name=title, author=author))
                    self.session.commit()
        for link in sup.find_all('a', 'sname f-fs1 s-fc0'):
            play_link = link.get("href").replace("/playlist?id=", "")
            play_name = link.get("title").encode('utf-8')
            if pysql.single("playlist163","link",play_link) == True:
                self.session.add(pysql.Playlist163(title=play_name, link=play_link, cnt=-1))
                self.session.commit()


if __name__ == "__main__":
    tmp = Comment()
    tmp.view_links(326735)
    tmp.views_capture(28793140, 1, 1)
    # tmp.viewsCapture(28793142,1,2)
