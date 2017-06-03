 ![spider163 logo](https://github.com/Chengyumeng/spider163/blob/master/logo.jpeg)
# 抓取网易云音乐 spider163 v2.0

## 安装模块
```
$ python setup.py install
```

## 查看帮助
```console
$ python capture.py --help
$ # 命令帮助相关内容
```

## 功能模块
- config
- createdb
- playlist
- music
- comment

## 使用指南

```console
$ python capture.py --module=config --config=spider163.conf
$ # 查看配置文件配置数据的详情和联通性
```
```console
$ python capture.py --module=createdb --config=spider163.conf
$ # 重建相关数据库
```
```console
$ python capture.py --module=playlist --config=spider163.conf --start=0 --end=39
$ # 指定起止页数下载歌单
```
```console
$ python capture.py --module=music --config=spider163.conf --source=db
$ # 从数据库导入歌单信息抓取音乐链接
```
```console
$ python capture.py --module=music --config=spider163.conf --source=cmd --playlist=720308660
$ # 下载歌单720308660
```
```console
$ python capture.py --module=comment --config=spider163.conf --source=db --maxval=10 --page=1
$ # 从数据库获取10首音乐的链接，抓取其首页的热评
```
```console
$ python capture.py --module=comment --config=spider163.conf --source=cmd --mid=28793140 --page=100
$ # 抓取歌曲28793140的一百页评论内的热评
```

## 过往版本
- [v0.9](https://github.com/Chengyumeng/spider163/tree/master/v0.9)

# 欢迎关注微信公众账号：程天写代码
![guojingcoooool](https://github.com/Chengyumeng/spider163/blob/master/wechat.jpeg)
