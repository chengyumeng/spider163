#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import json
from bs4 import BeautifulSoup
from pprint import pprint
import MySQLdb
import sys
import ConfigParser

def querySQL(cursor,sql):
    cursor.execute(sql)
    results = cursor.fetchall()
    return results
def isSingle(cursor,song_id):
    sql = "select song_id from music163 where song_id =" + str(song_id)
    cursor.execute(sql)
    results = cursor.fetchall()
    if len(results) == 0 :
        return True
    else :
        return False

def insertSQL(cursor,sql):
    try:
        cursor.execute(sql)
        db.commit()
    except:
        db.rollback()
def execData(cursor,url):
    s = requests.session()
    s = BeautifulSoup(s.get(play_url,headers = headers).content)
    try:
        musics = json.loads(s.find('textarea',{'style':'display:none;'}).text)
        for music in musics:
            name   = MySQLdb.escape_string(music['name'].encode('utf-8'))
            author = MySQLdb.escape_string(music['artists'][0]['name'].encode('utf-8'))
            sql = "insert into music163 (song_id,song_name,author) values (" + str(music['id']) + ",'" + name + "','"+ author + "')"
            if isSingle(cursor,music['id']) == True:
                print('{} : {}'.format(name,music['id']))
                cursor.execute(sql)
                db.commit()
            else :
                print('{} : {}'.format(name,"Not Single"))
    except :
        print('{}:{}'.format("Unexcept Error",url))


play_url = "http://music.163.com/playlist?id="    
headers = {
        'Referer':'http://music.163.com/',
        'Host':'music.163.com',
        'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
        }

cf = ConfigParser.ConfigParser()
cf.read('spider163.conf')
host = cf.get("db", "host")
user = cf.get("db", "user")
pawd = cf.get("db", "pass")
db = MySQLdb.connect(host,user,pawd,"spider" )
cursor = db.cursor()

if sys.argv[1] == "playlist":
    global play_url
    play_url = 'http://music.163.com/playlist?id='+ sys.argv[2]
    execData(cursor,play_url) 
elif sys.argv[1] == "database":
    cnt = 1024
    while cnt > 0 :
        sql = "select link,id from playlist163 where over = 'N' limit 100"
        results = querySQL(cursor,sql)
        cnt = len(results)
        for result in results:
            play_url = 'http://music.163.com' + str(result[0])
            execData(cursor,play_url)
            up_sql = "update playlist163 set over = 'Y' where id ="+ str(result[1])
            insertSQL(cursor,up_sql)
db.close()

