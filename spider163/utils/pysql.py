#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random

from sqlalchemy import Column, Integer, String, TIMESTAMP, Index, extract
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from sqlalchemy.dialects.mysql import MEDIUMTEXT

from spider163 import settings
from spider163.utils import pylog

Base = declarative_base()


class Playlist163(Base):
    __tablename__ = "playlist163"

    id = Column(Integer(), primary_key=True, autoincrement=True)
    title = Column(String(5000), server_default="System Title")
    link = Column(String(255), server_default="No Link")
    cnt = Column(Integer(), server_default="-1")
    dsc = Column(String(255), server_default="No Description")
    create_time = Column(TIMESTAMP, server_default=func.now())
    over = Column(String(255), server_default="N")
    over_link = Index("over_link", over, link)


class Music163(Base):
    __tablename__ = "music163"
    id = Column(Integer(), primary_key=True, autoincrement=True)
    song_id = Column(Integer())
    song_name = Column(String(5000), server_default="No Name")
    author = Column(String(3000), server_default="No Author")
    over = Column(String(255), server_default="N")
    has_lyric = Column(String(255), server_default="N")
    create_time = Column(TIMESTAMP, server_default=func.now())
    comment = Column(Integer(), server_default="-1")
    over_id = Index("over_id", over,id)
    key_author = Index("author", author)
    song_id_comment = Index("song_id_comment", song_id, comment)


class Comment163(Base):
    __tablename__ = "comment163"
    id = Column(Integer(), primary_key=True, autoincrement=True)
    song_id = Column(Integer())
    txt = Column(MEDIUMTEXT)
    author = Column(String(3000), server_default="No Author")
    liked = Column(Integer(), server_default="0")
    Index("liked_song_id", liked, song_id)
    Index("song_id_liked", song_id, liked)


class Lyric163(Base):
    __tablename__ = "lyric163"
    id = Column(Integer(), primary_key=True, autoincrement=True)
    song_id = Column(Integer())
    txt = Column(MEDIUMTEXT)
    key_song_id = Index("song_id", song_id)


def single(table, k, v):
    cnt = settings.engine.execute('select count(*) from ' + table + ' where ' + k + '=\'' + str(v) + '\'').fetchone()
    if cnt[0] == 0:
        return True
    else:
        return False


def stat_playlist():
    data = {}
    data["gdType"] = settings.Session.query(func.substring(Playlist163.dsc, 4, 2).label('type'), func.count('*').label('count')).group_by("type").all()
    data["gdOver"] = settings.Session.query(Playlist163.over.label('over'), func.count('*').label('count')).group_by("over").all()
    return data


def stat_music():
    data = {"author-comment-count": []}
    cd = settings.Session.query(Music163.author.label('author'), func.sum(Music163.comment).label('count')).group_by("author").order_by(func.sum(Music163.comment).label('count').label('count').desc()).limit(30).all()
    for m in cd:
        data["author-comment-count"].append([m[0], int(m[1])])
    data["music-comment-count"] = settings.Session.query(Music163.song_name, Music163.comment.label("count")).order_by(Music163.comment.label("count").desc()).limit(30).all()
    return data


def stat_data():
    data = {}
    data["countPlaylist"] = int(settings.engine.execute("select(select count(*) from playlist163 where over = 'Y')*100 / count(*) from playlist163").fetchone()[0]);
    data["countComment"] = int(settings.engine.execute("select(select count(*) from music163 where over = 'Y')*100 / count(*) from music163").fetchone()[0]);
    data["countLyric"] = int(settings.engine.execute("select(select count(*) from music163 where has_lyric = 'Y')*100 / count(*) from music163").fetchone()[0]);
    return data


def random_data():
    rng = settings.Session.query(func.min(Comment163.id), func.max(Comment163.id)).all()[0]
    data = []
    for i in range(12):
        v = random.uniform(rng[0], rng[1])
        d = settings.engine.execute("select txt,liked,a.author,song_name,a.song_id,b.author from comment163 a inner join music163 b on a.song_id= b.song_id where a.id>" +str(v) + " limit 1").fetchone()
        data.append({"txt": d[0],"like": d[1] ,"author": d[2],  "song" :{"name":d[3], "author": d[5], "id": d[4]}})
    return data


def initdb():
    try:
        Base.metadata.create_all(settings.engine)
    except Exception as e:
        pylog.print_warn("自动生成数据库表出现问题: {}".format(e))


def dropdb():
    try:
        Base.metadata.drop_all(settings.engine)
    except Exception as e:
        pylog.print_warn("自动删除数据库表出现问题: {}".format(e))

