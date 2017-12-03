#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask, request, json, jsonify
from flask import render_template, make_response

from spider163.spider import playlist
from spider163.spider import music
from spider163.spider import lyric
from spider163.spider import comment
from spider163.utils import pysql

app = Flask(__name__, static_path='/static')


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/spider")
def spider(type=None):
    return render_template('spider.html')


@app.route("/spider/getPlaylist", methods=['POST'])
def get_playlist():
    pl = playlist.Playlist()
    title = pl.view_capture(int(request.form['gdPage']),request.form["gdType"].encode("utf-8"))
    return jsonify({"type": request.form["gdType"],"title": title})


@app.route("/spider/getMusic", methods=['POST'])
def get_music():
    mu = music.Music()
    data = mu.views_capture(request.form["gdSource"].encode("utf-8"))
    return jsonify({"type": request.form["gdSource"],"data": data})


@app.route("/spider/getLyric", methods=["POST"])
def get_lyric():
    ly = lyric.Lyric()
    data = ly.view_lyrics(int(request.form["gqCount"]))
    return jsonify({"count": request.form["gqCount"],"data": data})


@app.route("/spider/getComment", methods=["POST"])
def get_comment():
    cm = comment.Comment()
    data = cm.auto_view(int(request.form["gqCount"]))
    return jsonify({"count": request.form["gqCount"],"data": data})


@app.route("/stat")
def statistics():
    return render_template('stat.html')


@app.route("/stat/playlist")
def stat_playlist():
    return jsonify(pysql.stat_playlist())


@app.route("/stat/music")
def stat_music():
    return jsonify(pysql.stat_music())


@app.route("/stat/dataCount")
def stat_data():
    return jsonify(pysql.stat_data())


@app.route("/scan")
def scan():
    return render_template('scan.html')


@app.route("/scan/data")
def scan_data():
    comment = pysql.random_data()
    if len(comment) > 0:
        res = {"msg":"ok","num":len(comment),"comment":comment}
        return jsonify(res)
    else:
        return jsonify({"msg":"ok","num":len(comment),"comment":[]})


@app.route("/bussiness")
def bussiness():
    return render_template('bussiness.html')




