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
def aesEncrypt(text, secKey):
    pad = 16 - len(text) % 16
    text = text + pad * chr(pad)
    encryptor = AES.new(secKey, 2, '0102030405060708')
    ciphertext = encryptor.encrypt(text)
    ciphertext = base64.b64encode(ciphertext)
    return ciphertext


def rsaEncrypt(text, pubKey, modulus):
    text = text[::-1]
    rs = int(text.encode('hex'), 16)**int(pubKey, 16) % int(modulus, 16)
    return format(rs, 'x').zfill(256)


def createSecretKey(size):
    return (''.join(map(lambda xx: (hex(ord(xx))[2:]), os.urandom(size))))[0:16]

def querySQL(cursor,sql):
    cursor.execute(sql)
    results = cursor.fetchall()
    return results

def insertSQL(cursor,sql):
    try:
        cursor.execute(sql)
        db.commit()
    except:
        db.rollback()


url = 'http://music.163.com/weapi/v1/resource/comments/R_SO_4_293940/?csrf_token='
headers = {
    'Cookie': 'appver=1.5.0.75771;',
    'Referer': 'http://music.163.com/'
    }
text = {
    'username': '13393376853',
    'password': 'wangyidafahao',
    'rememberLogin': 'true'
    }
modulus = '00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7'
nonce = '0CoJUm6Qyw8W8jud'
pubKey = '010001'
text = json.dumps(text)
secKey = createSecretKey(16)
encText = aesEncrypt(aesEncrypt(text, nonce), secKey)
encSecKey = rsaEncrypt(secKey, pubKey, modulus)
data = {
    'params': encText,
    'encSecKey': encSecKey
    }

cf = ConfigParser.ConfigParser()
cf.read('spider163.conf')
host = cf.get("db", "host")
user = cf.get("db", "user")
pawd = cf.get("db", "pass")
db = MySQLdb.connect(host,user,pawd,"spider" )
cursor = db.cursor()
if __name__ == "__main__":
    if len(sys.argv) > 1:
        for idx in range(len(sys.argv)):
            if idx > 0:
                song_id = sys.argv[idx]
                dele = "delete from comment163 where song_id=" + song_id
                url = "http://music.163.com/weapi/v1/resource/comments/R_SO_4_" + song_id + "/?csrf_token="
                insertSQL(cursor,dele)
                try:
                    req = requests.post(url, headers=headers, data=data)
                    for comment in req.json()['comments']:
                        insertSQL(cursor,"insert into comment163 (song_id,txt,author,liked) values (" + song_id + ",'" + MySQLdb.escape_string(comment['content'].encode('utf-8')) + "','" + MySQLdb.escape_string(comment['user']['nickname'].encode('utf-8')) + "'," + str(comment['likedCount']) +")" )
                    for comment in req.json()['hotComments']:
                        insertSQL(cursor,"insert into comment163 (song_id,txt,author,liked) values (" + song_id + ",'" + MySQLdb.escape_string(comment['content'].encode('utf-8')) + "','" + MySQLdb.escape_string(comment['user']['nickname'].encode('utf-8')) + "'," + str(comment['likedCount']) +")" )
                except:
                    print "ERROR" + song_id
                insertSQL(cursor,"update music163 set over = 'Y',comment=" + str(req.json()['total']) + " where song_id=" + song_id)
    else:
        cnt = 1024
        while cnt > 0 :
            sql = "select song_id from music163 where over = 'N' limit 100"
            results = querySQL(cursor,sql)
            cnt = len(results)
            if cnt > 0 :
                for result in results:
                    url = "http://music.163.com/weapi/v1/resource/comments/R_SO_4_" + str(result[0])+"/?csrf_token="
                    try:
                        req = requests.post(url, headers=headers, data=data)
                        for comment in req.json()['comments']:
                            insertSQL(cursor,"insert into comment163 (song_id,txt,author,liked) values (" + str(result[0]) + ",'" + MySQLdb.escape_string(comment['content'].encode('utf-8')) + "','" + MySQLdb.escape_string(comment['user']['nickname'].encode('utf-8')) + "'," + str(comment['likedCount']) +")" )
                        for comment in req.json()['hotComments']: 
                            insertSQL(cursor,"insert into comment163 (song_id,txt,author,liked) values (" + str(result[0]) + ",'" + MySQLdb.escape_string(comment['content'].encode('utf-8')) + "','" + MySQLdb.escape_string(comment['user']['nickname'].encode('utf-8')) + "'," + str(comment['likedCount']) +")" )
                    except:
                        print "ERROR" + str(result[0])
                    print req.json()['total']
                    insertSQL(cursor,"update music163 set over ='Y',comment="+ str(req.json()['total'])+ " where song_id = " + str(result[0]))
db.close()
