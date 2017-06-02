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


class Music:
    
    def __init__(self):
        self.__headers = {
        'Referer':'http://music.163.com/',
        'Host':'music.163.com',
        'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
        }
        self.__db  = db.MySQLDB()
        self.__url = "http://music.163.com"

    def viewCapture(self,link):
        url = self.__url + str(link)
        s = requests.session()
        s = BeautifulSoup(s.get(url,headers = self.__headers).content,"lxml")
        try:
            musics = json.loads(s.find('textarea',{'style':'display:none;'}).text)
            for music in musics:
                name   = MySQLdb.escape_string(music['name'].encode('utf-8'))
                author = MySQLdb.escape_string(music['artists'][0]['name'].encode('utf-8')) 
                sql = "insert into music163 (song_id,song_name,author) values (" + str(music['id']) + ",'" + name + "','"+ author + "')"
                if self.isSingle(music['id']) == True:
                    self.__db.insertSQL(sql)
                else :
                    print('{}:{}'.format(name,"Not Single"))
        except:
            print('{} : {}'.format("Unexcept Error",url))

    def isSingle(self,song_id):
        sql = "select song_id from music163 where song_id =" + str(song_id)
        rts = self.__db.querySQL(sql)
        if len(rts) > 0 :
            return False
        else :
            return True


# if __name__ == "__main__":
#     tmp = Music()
#     tmp.viewCapture("/playlist?id=739396417")
