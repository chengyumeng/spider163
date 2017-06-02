#!/usr/bin/env python
# -*- coding: utf-8 -*-

import ConfigParser
import MySQLdb

def singletan(cls):
    instance = cls()
    instance.__call__ = lambda : instance
    return instance

@singletan
class MySQLDB:
    __db     = None
    __cursor = None

    def __init__(self):
        cf = ConfigParser.ConfigParser()
        cf.read('../spider163.conf')
        host = cf.get("mysql", "host")
        username = cf.get("mysql", "username")
        password = cf.get("mysql", "password")
        database = cf.get("mysql", "database")
        self.__db     = MySQLdb.connect(host,username,password,database)
        self.__cursor = self.__db.cursor()
        self.__cursor.execute("SET NAMES utf8mb4")
        self.__db.commit()

    def createTables(self):
        playlist = "CREATE TABLE `playlist1631` (`id` int(11) NOT NULL AUTO_INCREMENT,`title` varchar(150) DEFAULT '',`link` varchar(120) DEFAULT '',`cnt` varchar(20) DEFAULT '0',`dsc` varchar(50) DEFAULT 'all',`create_time` datetime DEFAULT CURRENT_TIMESTAMP,`over` varchar(20) DEFAULT 'N',PRIMARY KEY (`id`),KEY `over_link` (`over`,`link`)) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8"
        music    = "CREATE TABLE `music1631` (`id` int(11) NOT NULL AUTO_INCREMENT,`song_id` int(11) DEFAULT NULL,`song_name` varchar(200) DEFAULT '',`author` varchar(350) DEFAULT '',`over` varchar(5) DEFAULT 'N',`create_time` datetime DEFAULT CURRENT_TIMESTAMP,`comment` int(11) DEFAULT '0',PRIMARY KEY (`id`),KEY `over_id` (`over`,`id`),KEY `author` (`author`),KEY `song_id_comment` (`song_id`,`comment`)) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8"
        comment  = "CREATE TABLE `comment1631` (`id` int(11) NOT NULL AUTO_INCREMENT,`song_id` int(11) DEFAULT NULL,`txt` mediumtext,`author` varchar(100) DEFAULT '注销', `liked` int(11) DEFAULT '0',PRIMARY KEY (`id`), KEY `liked_song_id` (`liked`,`song_id`), KEY `song_id_liked` (`song_id`,`liked`)) ENGINE=InnoDB AUTO_INCREMENT=1418975 DEFAULT CHARSET=utf8"  
        self.__cursor.execute(playlist)
        self.__cursor.execute(music)
        self.__cursor.execute(comment)

    
    def querySQL(self,sql):
        self.__cursor.execute(sql)
        results = self.__cursor.fetchall()
        return results
    
    def insertSQL(self,sql):
        try:
            self.__cursor.execute(sql)
            self.__db.commit()
        except:
            self.__db.rollback()
            print("SQL ERROR |" + sql)

    def getRange(self,table,column = "id"):
        sql = "select min(" + column + "),max(" + column + ") from " + table 
        rng = self.querySQL(sql)
        if len(rng) > 0 and len(rng[0]) == 2:
            return rng[0]
        else:
            return [0,0]


    def __del__(self):
        self.__db.close()
        print("-- [MySQL] | Has Been Closed --")

if __name__ == "__main__":
    tmp = MySQLDB()
    tmp.createTables()
    print("创建相应数据库表")
