# -*- coding: utf-8 -*-

from cement.core.foundation import CementApp
from cement.core.controller import CementBaseController, expose
from colorama import Fore
from colorama import init
from spider163.utils import pysql
from spider163.spider import playlist
from spider163.spider import music
from spider163.spider import comment
from spider163.spider import lyric
from spider163.spider import search
import time

VERSION = '2.4.7'

BANNER = """
Spider163 Application v%s
Copyright (c) 2017 Cheng Tian Enterprises
Welcome to Follow My 【微信公众账号】"程天写代码"
""" % VERSION

init(autoreset=True)

class VersionController(CementBaseController):
    class Meta:
        label = 'base'
        description = 'Spider163是Github上最流行的网易云音乐爬虫系统'
        arguments = [
            (['-v', '--version'], dict(action='version', version=BANNER)),
            ]


class DatabaseController(CementBaseController):
    class Meta:
        label = "database"
        description = "数据库相关操作"
        arguments = []

    @expose(help="自动生成数据库相关依赖")
    def initdb(self):
        print("正在生成全部数据库表结构……")
        pysql.initdb()

    @expose(help="重置数据库配置")
    def resetdb(self):
        print("正在删除全部已下载数据……")
        pysql.dropdb()
        pysql.initdb()


class SpiderController(CementBaseController):
    class Meta:
        label = "spider"
        description = "爬虫-蜘蛛等相关操作"
        arguments = [
            (['-p', '--page'],
             dict(help="抓取的页码")),
            (['-c', '--count'],
             dict(help="")),
            (['-s', '--song'],
             dict(help="歌曲ID")),
            (['--classify'],
             dict(help="风格")),
        ]

    @expose(help="获取全部歌曲风格列表(作为抓取歌单的参照)")
    def classify(self):
        playlist.Playlist().get_classify()

    @expose(help="根据推荐歌单抓取网易云音乐歌单数据(-p --page | --classify)")
    def playlist(self):
        pg = self.app.pargs.page
        cf = "全部"
        pl = playlist.Playlist()
        if self.app.pargs.classify !=None:
            cf = self.app.pargs.classify
        if pg != None:
            print(Fore.GREEN + '正在抓取 曲风为 {} 的第 {} 页歌单……'.format(cf, pg))
            pl.view_capture(int(pg), cf)
        else:
            for i in range(36):
                print(Fore.GREEN + '正在抓取 曲风为 {} 的第 {} 页歌单……'.format(cf ,i + 1))
                pl.view_capture(i + 1, cf)

    @expose(help="通过歌单抓取网易云音乐歌曲，单次抓取歌单10个(-c --count)")
    def music(self):
        msc = music.Music()
        if self.app.pargs.count  == None:
            msc.views_capture()
            return
        cnt = int(self.app.pargs.count)
        if cnt <= 0:
            print(Fore.RED + "不合法的--count -c 变量（ > 0 ）")
        else:
            for i in range(cnt):
                print(Fore.GREEN + '正在执行第 {} 批抓取计划，本次抓取歌单歌曲 10 个\r\n'.format(i + 1))
                msc.views_capture()

    @expose(help="通过音乐列表抓取网易云音乐热评，单次抓取音乐1首(-c --count),也可以指定歌曲ID(-s --song)")
    def comment(self):
        cmt = comment.Comment()
        if self.app.pargs.song != None:
            print(Fore.BLUE + '正在执行抓取歌曲 {} 热门评论计划'.format(self.app.pargs.song))
            cmt.view_capture(int(self.app.pargs.song), 1)
            print(Fore.GREEN + '抓取完成\r\n')
            return
        if self.app.pargs.count != None:
            print(Fore.GREEN + '正在执行批量抓取热门评论计划，本次计划抓取歌曲 {} 首\r\n'.format(self.app.pargs.count))
            cmt.auto_view(int(self.app.pargs.count))
        else:
            cmt.auto_view(1)

    @expose(help="通过音乐列表抓取网易云音乐歌词,可以指定抓取歌曲数量（-c --count），也可以指定歌曲ID（-s --song）")
    def lyric(self):
        lrc = lyric.Lyric()
        if self.app.pargs.song != None:
            print(Fore.BLUE + '正在执行抓取歌曲 {} 歌词的计划'.format(self.app.pargs.song))
            lrc.view_lyric(self.app.pargs.song)
            print(Fore.GREEN + '抓取完成\r\n')
        elif self.app.pargs.count != None:
            print(Fore.GREEN + '正在执行批量抓取歌词计划，本次计划抓取歌曲 {} 首\r\n'.format(self.app.pargs.count))
            lrc.view_lyrics(int(self.app.pargs.count))
        else:
            print("您至少指定--song或者--count一个参数")


class QueryController(CementBaseController):
    class Meta:
        label = "query"
        stacked_on = 'base'
        description = "爬虫-蜘蛛等相关操作"
        arguments = [
            (['--playlist'],
             dict(help="")),
            (['-q', '--query'],
             dict(help="")),
        ]

    @expose(help="通过歌单ID和歌曲ID获取歌单、歌曲相关信息（--song --playlist）")
    def get(self):
        if self.app.pargs.song != None:
            comment.Comment().get_music(self.app.pargs.song)
            lyric.Lyric().get_lyric(self.app.pargs.song)
        if self.app.pargs.playlist != None:
            music.Music().get_playlist(self.app.pargs.playlist)

    @expose(help="搜索功能(-q --query)")
    def search(self):
        if self.app.pargs.query != None:
            search.searchSong(self.app.pargs.query)
            search.searchAlbum(self.app.pargs.query)
            search.searchSinger(self.app.pargs.query)
            search.searchPlaylist(self.app.pargs.query)


class WebController(CementBaseController):
    class Meta:
        label = "web"
        stacked_on = 'base'
        description = "网络平台"
        arguments = [
        ]

    @expose(help="测试-未开放")
    def webserver(self):
        while True:
            time.sleep(5)
            print("该功能尚未完成")


class App(CementApp):
    class Meta:
        label = "Spider163"
        base_controller = "base"
        handlers = [VersionController, DatabaseController, SpiderController, QueryController, WebController]




