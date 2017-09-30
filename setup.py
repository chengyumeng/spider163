#!/usr/bin/env python
# -*- coding: utf-8 -*

from setuptools import setup, find_packages

setup(
      version="2.1",
      name='spider163',
      author='Chengyumeng',
      url='https://github.com/Chengyumeng/spider163',
      author_email='doublexuan.top@gmail.com',
      packages=find_packages(),
      scripts=['spider163/bin/spider163'],
      install_requires=[
            "beautifulsoup4==4.6.0",
            "bs4==0.0.1",
            "cement==2.10.2",
            "certifi==2017.7.27.1",
            "chardet==3.0.4",
            "idna==2.6",
            "MySQL-python==1.2.5",
            "Naked==0.1.31",
            "pprint==0.1",
            "progressbar==2.3",
            "pycrypto==2.6.1",
            "PyYAML==3.12",
            "requests==2.18.4",
            "shellescape==3.4.1",
            "SQLAlchemy==1.1.14",
            "terminaltables==3.1.0",
            "urllib3==1.22"
      ]

)
