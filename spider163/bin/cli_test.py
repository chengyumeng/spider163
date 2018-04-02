import unittest

from spider163.spider import playlist
from spider163.spider import mp3
from spider163.spider import search
from spider163.spider import read
from spider163.utils import healthz


class TestStringMethods(unittest.TestCase):

    def test_config(self):
        healthz.is_correct_config()
        healthz.is_correct_db()
        healthz.can_spider()

    def test_classify(self):
        playlist.Playlist().get_classify()

    def test_mp3(self):
        m = mp3.MP3()
        m.view_down(2127220577, "./test")

    def test_search(self):
        search.searchSong("李荣浩")
        search.searchAlbum("韩寒")
        search.searchSinger("林依晨")
        search.searchPlaylist("SHE")

    def test_doc(self):
        read.print_pdf(2127220577)


if __name__ == '__main__':
    unittest.main()