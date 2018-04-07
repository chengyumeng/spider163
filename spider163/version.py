# -*- coding: utf-8 -*-
import os
import sys

PYTHON3 = False
if sys.version > "3":
    PYTHON3 = True

VERSION = "2.7.6"
DESCRIPTION = """
Spider163的数据基础，来源于网易公司的网易云音乐产品。其授权协议，包含《网易云音乐服务条款》但不包含其霸王条款。

该项目遵循MIT开源协议。我们认为知识属于全人类，网易云音乐的评论区属于用户，不属于网易云音乐。

而广大网民有权利根据自己的喜好阅读、整理、分析和总结开放的、非私密信息。


您可以选择四种方式支持本项目的开发：

No.1 在Github上star本项目，或者在其它任何场合宣传本项目。

附：Spider163 GitHub 地址 https://github.com/Chengyumeng/spider163

No.2 关注本项目作者的唯一个人微信公众账号。

公众号名字：程天写代码

No.3 通过支付宝向作者转账赞助。

支付宝二维码：https://github.com/Chengyumeng/spider163/blob/master/spider163/www/static/img/zhifubao.jpeg

No.4 通过微信向作者转账赞助。

微信二维码：https://github.com/Chengyumeng/spider163/blob/master/spider163/www/static/img/weixin.jpeg

"""
root_path = os.path.dirname(os.path.abspath(__file__))

MAILBODY = """
<h2 style="color: #C20C0C; margin: 10px 0;"><a href="https://github.com/Chengyumeng/spider163" target="_blank">Spider163</a> 云音乐今日精彩推荐(微信公众号：pod1024)</h2>
<h2 style="color: #C20C0C; margin: 10px 0;"></h2>
<p  style="color: #C10B0B; margin: 10px 0;" >今日分享评论数量排行 {} - {} 歌曲：</p>
<ul>{}</ul>
<div style="margin: 20px 0 0 0;">
<p style="font-weight: 400;font-style: normal;font-size: 30px;color: #333;text-align: center;margin: 30px auto;">欢迎关注程天写代码微信公众号：pod1024</p>
</div>
"""

MAILMUSIC = """
<li><span style="font-weight: bold; margin: 2px 10px 5px 10px;"><a href="http://music.163.com/#/song?id={}" target="_blank">{}</a></span>
<span style="font-weight: bold; margin: 2px 10px 5px 10px;">{}</span> 
<span style="font-weight: bold; margin: 2px 10px 5px 10px;">评论数：{}</span></li><hr>
{}
"""
MAILCOMMENT = """
<p><span style="font-weight: bold; margin: 2px 10px 5px 10px;color: #a40011;">{}</span> 
<span style="font-weight: bold; margin: 2px 10px 5px 10px;color:">{} :</span> </p>
<p style="margin: 12px 20px 15px 20px;">{}</p>
"""
