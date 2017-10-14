#!/usr/bin/env python
# -*- coding: utf-8 -*-

import settings as uapi
import requests
from bs4 import BeautifulSoup
from terminaltables import AsciiTable

from spider163.utils import pysql
from spider163.utils import pylog
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
        try:
            acmsk = {'class': 'msk'}
            scnb = {'class': 'nb'}
            dcu = {'class': 'u-cover u-cover-1'}
            ucm = {'class': 'm-cvrlst f-cb'}
            s = BeautifulSoup(s.get(play_url, headers=self.__headers).content, "html.parser")
            lst = s.find('ul', ucm)
            for play in lst.find_all('div', dcu):
                title = play.find('a', acmsk)['title'].encode('utf-8')
                link = play.find('a', acmsk)['href'].encode('utf-8').replace("/playlist?id=", "")
                cnt = play.find('span', scnb).text.encode('utf-8').replace('万', '0000')
                if pysql.single("playlist163","link",link) == True:
                    pl = pysql.Playlist163(title=title, link=link, cnt=int(cnt), dsc="曲风：{}".format(type))
                    self.session.add(pl)
                    self.session.commit()
        except Exception:
            pylog.log.error("抓取歌单出现问题，歌单页码：" + str(page))
            raise


if __name__ == "__main__":
    tmp = Playlist()
    tmp.view_capture(2)

