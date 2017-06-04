#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import json
from bs4 import BeautifulSoup
from pprint import pprint
import MySQLdb
import db
import sys
import ConfigParser
import common as c

class Music:
    
    def __init__(self,config = "spider163.conf"):
        self.__headers = {
        'Referer':'http://music.163.com/',
        'Host':'music.163.com',
        'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
        }
        self.__db  = db.MySQLDB()
        if config != "spider163.conf":
            self.__db.setConfig()
        self.__url = "http://music.163.com"

    def viewsCapture(self):
        urls = self.__db.querySQL("select link from playlist163 where over = 'N' limit 10")
        for url in urls:
            self.viewCapture(url[0])
        for url in urls:
            self.__db.insertSQL("update playlist163 set over = 'Y' where link = '" + str(url[0]) + "'")
        return len(urls)

    def viewCapture(self,link):
        self.__db.insertSQL("update playlist163 set over = 'N' where link = '" + link + "'")
        url = self.__url + str(link)
        
        s = requests.session()
        try:
            s = BeautifulSoup(s.get(url,headers = self.__headers).content,"lxml")
            musics = json.loads(s.find('textarea',{'style':'display:none;'}).text)
            for music in musics:
                name   = MySQLdb.escape_string(music['name'].encode('utf-8'))
                author = MySQLdb.escape_string(music['artists'][0]['name'].encode('utf-8')) 
                sql = "insert into music163 (song_id,song_name,author) values (" + str(music['id']) + ",'" + name + "','"+ author + "')"
                if self.isSingle(music['id']) == True:
                    self.__db.insertSQL(sql)
                else :
                    c.Log('{} : {} {}'.format("ERROR 103",name,"Not Single"))
                self.__db.insertSQL("update playlist163 set over = 'Y' where link = '" + str(link) + "'")
        except:
            c.Log('{} : {}'.format("Error 901",url))

    def isSingle(self,song_id):
        sql = "select song_id from music163 where song_id =" + str(song_id)
        rts = self.__db.querySQL(sql)
        if len(rts) > 0 :
            return False
        else :
            return True

    def getPlaylistRange(self):
        rts = self.__db.querySQL("select count(*) from playlist163 where over = 'N'")
        return rts[0][0]


# if __name__ == "__main__":
#     tmp = Music()
#     tmp.viewCapture("/playlist?id=739396417")
