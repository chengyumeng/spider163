#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
from terminaltables import AsciiTable

from spider163.utils import pysql
from spider163.utils import pylog
from spider163.utils import tools

from spider163.spider import public as uapi
from spider163 import settings


class Playlist:
    __play_url = None
    __headers = None

    def __init__(self):
        self.__headers = uapi.header
        self.__play_url = uapi.play_url
        self.session = settings.Session()

    def get_classify(self):
        table = [["类别", "风格列表"]]
        for k, v in uapi.classify.items():
            c = 0
            lst = ""
            for v in v:
                c = c + 1
                if c % 5 == 0:
                    lst = lst + v + "\n"
                else:
                    lst = lst + v + ","
            table.append([k, lst])
        print(AsciiTable(table).table)

    def view_capture(self, page, type="全部"):
        s = requests.session()
        play_url = self.__play_url.format(type, page * 35)
        titles = []
        try:
            acmsk = {'class': 'msk'}
            scnb = {'class': 'nb'}
            dcu = {'class': 'u-cover u-cover-1'}
            ucm = {'class': 'm-cvrlst f-cb'}
            s = BeautifulSoup(s.get(play_url, headers=self.__headers).content, "html.parser")
            lst = s.find('ul', ucm)
            for play in lst.find_all('div', dcu):
                title = tools.encode(play.find('a', acmsk)['title'])
                link = tools.encode(play.find('a', acmsk)['href']).replace("/playlist?id=", "")
                cnt = tools.encode(play.find('span', scnb).text).replace('万', '0000')
                if pysql.single("playlist163","link",link) is True:
                    pl = pysql.Playlist163(title=title, link=link, cnt=int(cnt), dsc="曲风：{}".format(type))
                    self.session.add(pl)
                    self.session.commit()
                    titles.append(title)
            return titles
        except Exception as e:
            pylog.log.error("抓取歌单出现问题：{} 歌单类型：{} 页码：{}".format(e, type, page))
            raise
