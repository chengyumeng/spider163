#!/usr/bin/env python
# -*- coding: utf-8 -*-

from spider163 import db
from spider163 import comment
from spider163 import music
from spider163 import playlist
from progressbar import ProgressBar
import click

@click.command()
@click.option("--module",type = click.Choice(['config']))
@click.option("--config",default = "spider163.conf",help = "the location of the loaded configuration file")
def displayConfig(config,module = "config"):
    dbs = db.MySQLDB()
    if config !="spider163.conf":
        dbs.setConfig(str(config))
    dbs.displayConfig()

@click.command()
@click.option('--config',default = "spider163.conf",help = "the location of the loaded configuration file")
@click.option("--module",type = click.Choice(['createdb']))
def createDB(config,module="createdb"):
    dbs = db.MySQLDB()
    if config !="spider163.conf":
        dbs.setConfig(str(config))
    dbs.createTables()

@click.command()
@click.option('--config',default = "spider163.conf",help = "the location of the loaded configuration file")
@click.option('--start',default = 0,help = "the start page for captured playlists")
@click.option('--end',default = 39,help = "the end page for captured playlists")
@click.option("--module",type = click.Choice(['playlist']))
def capturePlaylist(config,start,end,module="playlist"):
    pl = playlist.Playlist(str(config))
    pbar  = ProgressBar( maxval = (end - start + 1))
    pbar.start()
    while start<=end:
        pl.viewCapture(start)
        pbar.update(start)
        start = start + 1
    pbar.finish()
@click.command()
@click.option('--config',default = "spider163.conf",help = "the location of the loaded configuration file")
@click.option('--source',default = "db",help = "the source of the playlist,you can insert db(mysql) or cmd(command line)")
@click.option('--playlist',default = -1, help = "the playlist id if choose command input")
@click.option("--module",type = click.Choice(['music']))
def captureMusic(config,source,playlist,module = 'music'):
    msc = music.Music(str(config))
    if str(source) == "db":
        rng  = msc.getPlaylistRange() 
        step = 1024
        scss = 0
        pbar = ProgressBar(maxval = rng + 1)
        pbar.start()
        while step > 0 :
            step = msc.viewsCapture()
            scss = scss + step
            pbar.update(scss)
        pbar.finish()
    elif str(source) == "cmd":
        if playlist == -1 :
            print("unaailable playlist id : -1")
        else:
            msc.viewCapture("/playlist?id=" + str(playlist))
    else:
        print("unavailable value of source " + str(source))

@click.command()
@click.option('--config',default = "spider163.conf",help = "the location of the loaded configuration file")
@click.option('--source',default = "db", help = "the source of the playlist,you can insert db(mysql) or cmd(command line)")
@click.option('--mid',default = -1,help = "the music id if choose command input")
@click.option('--maxval',default = 100,help = "the quantity of capturing music")
@click.option('--page',default = 1,help = "for each piece of music, the number of pages that perform the crawl (default is one page)")
@click.option('--module',type = click.Choice(['comment']))
def captureComment(config,source,mid,maxval,page,module = 'comment'):
    cmt = comment.Comment(str(config))
    if str(source) == "db":
        pbar = ProgressBar(maxval = maxval + 1)
        pbar.start()
        scss = 0
        if maxval < 100:
            step = maxval
        else:
            step = 100
        while step > 0 :
            ids = cmt.getSongIDs(step)
            for item in ids :
                cmt.viewsCapture(item[0],1,page)
                pbar.update(scss)
                scc = scss + 1
            step = len(ids)
        pbar.finish()
    elif str(source) == "cmd":
        pbar = ProgressBar(maxval = page + 5)
        pbar.start()
        p = 1
        while p <= page:
            cmt.viewCapture(mid,p)
            pbar.update(p-1)
            p = p + 1
        pbar.finish()
    else:
        print("unavailable value of source " + str(source))

@click.command()
@click.option('--module',default = "config",help = " choose a function")
@click.option('--config',default = "spider163.conf",help = "the location of the loaded configuration file")
@click.option('--start',default = 0,help = "the start page for captured playlists")
@click.option('--end',default = 39,help = "the end page for captured playlists")
@click.option('--source',default = "db",help = "the source of the playlist,you can insert db(mysql) or cmd(command line)")
@click.option('--playlist',default = -1, help = "the playlist id if choose command input")
@click.option('--mid',default = -1,help = "the music id if choose command input")
@click.option('--maxval',default = 100,help = "the quantity of capturing music")
@click.option('--page',default = 1,help = "for each piece of music, the number of pages that perform the crawl (default is one page)")
def cmd(module,start,end,source,playlist,mid,maxval,page,config):
    if module == "createdb":
        createDB()
    elif module == "playlist":
        capturePlaylis()
    elif module == "music":
        captureMusic()
    elif module == "comment":
        captureComment()
    elif module == "config":
        displayConfig()
    else :
        print("ERROR")




if __name__ == "__main__":
    cmd()
    # createDB()
    # capturePlaylist()
    # captureMusic()
    # captureComment()




