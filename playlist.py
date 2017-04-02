#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import json
from bs4 import BeautifulSoup
from pprint import pprint
import MySQLdb
import sys
import ConfigParser

def insertSQL(cursor,sql):
    try:
        cursor.execute(sql)
        db.commit()
    except:
        db.rollback()
def queryLink(cursor,link):
    sql = "select * from playlist163 where link = '" + MySQLdb.escape_string(link) + "'"
    cursor.execute(sql)
    results = cursor.fetchall()
    if len(results) > 0 :
        return True
    else :
        return False

def execData(url,cursor):
    s = requests.session()
    s = BeautifulSoup(s.get(play_url,headers = headers).content)
    lst = s.find('ul',{'class':'m-cvrlst f-cb'})
    try :
        for play in lst.find_all('div',{'class':'u-cover u-cover-1'}):
            title = MySQLdb.escape_string(play.find('a',{'class':'msk'})['title'].encode('utf-8'))
            link  = MySQLdb.escape_string(play.find('a',{'class':'msk'})['href'].encode('utf-8'))
            cnt   = MySQLdb.escape_string(play.find('span',{'class':'nb'}).text.encode('utf-8'))
            sql   = "insert into playlist163 (title,link,cnt) values ('"+ title + "','" + link + "','" + cnt + "')";
            if queryLink(cursor,link) == False :
                insertSQL(cursor,sql)
                print('{} : {} :{}'.format(title,link,cnt))
            else :
                print('{} : {}'.format(link,"Same"))
    except:
        print('{} : {}'.format(play_url, "Trouble"))



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
if len(sys.argv) == 3 :
    global play_url
    start = int(sys.argv[1])
    end   = int(sys.argv[2])
    while start<= end:
        play_url = "http://music.163.com/discover/playlist/?order=hot&cat=全部&limit=35&offset=" + str(start*35)
        start = start + 1
        execData(play_url,cursor)
elif len(sys.argv) == 4 :
    global play_url
    cat   = sys.argv[1]
    start = int(sys.argv[2])
    end   = int(sys.argv[3])
    while start<=end:
        play_url = "http://music.163.com/discover/playlist/?order=hot&cat=" + cat + "&limit=35&offset=" + str(start*35)
        start = start + 1
        execData(play_url,cursor)
else :
    play_url = "http://music.163.com/discover/playlist/?order=hot&cat=全部&limit=35&offset=0"
    execData(play_url,cursor)
db.close()
