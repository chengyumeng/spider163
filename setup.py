#!/usr/bin/env python
# -*- coding: utf-8 -*

from setuptools import setup, find_packages, Command
import os
import imp


class CleanCommand(Command):
    """Custom clean command to tidy up the project root."""
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        os.system('rm -vrf ./build ./dist ./*.pyc ./*.tgz ./*.egg-info')


py3 = imp.load_source(
    'spider163.version', os.path.join('spider163', 'version.py')).PYTHON3

version = imp.load_source(
    'spider163.version', os.path.join('spider163', 'version.py')).VERSION
desc = imp.load_source(
    'spider163.version', os.path.join('spider163', 'version.py')).DESCRIPTION

install_requires = [
    "beautifulsoup4==4.6.0",
    "bs4==0.0.1",
    "cement==2.10.2",
    "certifi==2017.7.27.1",
    "chardet==3.0.4",
    "idna==2.6",
    "Naked==0.1.31",
    "pprint==0.1",
    "cryptography==2.3",
    "PyYAML==3.12",
    "requests==2.20.0",
    "shellescape==3.4.1",
    "SQLAlchemy==1.1.15",
    "SQLAlchemy-Utils==0.32.18",
    "terminaltables==3.1.0",
    "urllib3==1.24.2",
    "Logbook==1.1.0",
    "colorama==0.3.9",
    "flask==1.0",
    "python-docx==0.8.6",
    "xlwt==1.3.0"
]

if py3 is True:
    install_requires.append("mysqlclient==1.3.12")
else:
    install_requires.append("MySQL-python==1.2.5")


setup(
      version=version,
      name='spider163',
      author='ChengTian',
      description='简单易用、功能强大的网易云音乐爬虫',
      long_description=desc,
      entry_points={
        "console_scripts": ["spider163=spider163.bin.cli:main"]
      },
      url='https://github.com/Chengyumeng/spider163',
      author_email='792400644@qq.com',
      packages=find_packages(),
      include_package_data=True,
      license='MIT License',
      zip_safe=False,
      install_requires=install_requires,
      classifiers=[
            'Development Status :: 5 - Production/Stable',
            'Environment :: Console',
            'Environment :: Web Environment',
            'Programming Language :: Python :: 2.7',
            'Programming Language :: Python :: 3.4',
      ],
      cmdclass={
            'clean': CleanCommand,
      },

)
