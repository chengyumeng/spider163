#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import json
from bs4 import BeautifulSoup
from pprint import pprint
import db
import MySQLdb
import sys
import ConfigParser
from progressbar import ProgressBar

class Playlist:
    __db = None
    __play_url = None
    __headers  = None
    def __init__(self):
        self.__headers = {
        'Referer':'http://music.163.com/',
        'Host':'music.163.com',
        'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
        }
        self.__db = db.MySQLDB()
        self.__play_url = "http://music.163.com/discover/playlist/?order=hot&cat=全部&limit=35&offset="

    def viewCapture(self,page):
        s = requests.session()
        play_url = self.__play_url + str(page * 35)
        try :
            s = BeautifulSoup(s.get(play_url,headers = self.__headers).content,"lxml")
            lst = s.find('ul',{'class':'m-cvrlst f-cb'})
            for play in lst.find_all('div',{'class':'u-cover u-cover-1'}):
                title = MySQLdb.escape_string(play.find('a',{'class':'msk'})['title'].encode('utf-8'))
                link  = MySQLdb.escape_string(play.find('a',{'class':'msk'})['href'].encode('utf-8'))
                cnt   = MySQLdb.escape_string(play.find('span',{'class':'nb'}).text.encode('utf-8'))
                sql   = "insert into playlist163 (title,link,cnt) values ('"+ title + "','" + link + "','" + cnt + "')";
                if self.queryLink(link) == False :
                    self.__db.insertSQL(sql)
        except:
            print('{} : {}'.format(play_url, "Trouble"))

    def queryLink(self,link):
    	sql = "select * from playlist163 where link = '" + MySQLdb.escape_string(link) + "'"
        results = self.__db.querySQL(sql)
        if len(results) > 0 :
            return True
        else :
            return False

# if __name__ == "__main__":
# 	tmp = Playlist()
# 	tmp.viewCapture(1)
        
