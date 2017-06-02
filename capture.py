#!/usr/bin/env python
# -*- coding: utf-8 -*-

from spider163 import db
from spider163 import comment
from spider163 import music
from spider163 import playlist
from progressbar import ProgressBar
import click

@click.command()
@click.option('--config',default = "spider163.conf",help = "the location of the loaded configuration file")
def createDB(config):
    print("创建数据库表结构 配置文件为：" + str(config))
    dbs = db.MySQLDB()
    if config !="spider163.conf":
        pl.setConfig(str(config))
    dbs.createTables()

@click.command()
@click.option('--config',default = "spider163.conf",help = "the location of the loaded configuration file")
@click.option('--start',default = 0,help = "the start page for captured playlists")
@click.option('--end',default = 39,help = "the end page for captured playlists")
def capturePlaylist(config,start,end):
    pl = playlist.Playlist(str(config))
    pbar  = ProgressBar( maxval = (end - start + 1))
    pbar.start()
    while start<=end:
        pl.viewCapture(start)
        pbar.update(start)
        start = start + 1
    pbar.finish()

def captureMusic(config):
    print("爬取歌曲")

def captureComment(config):
    print("爬取评论")

if __name__ == "__main__":
    # createDB()
    capturePlaylist()




