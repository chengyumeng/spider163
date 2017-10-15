#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, request

app = Flask(__name__)


@app.route("/")
def index():
    return "聚合网易云音乐热评"


