#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
from spider163.utils import config
from logbook import FileHandler, Logger
from terminaltables import AsciiTable
from colorama import Fore
from colorama import init

path = config.get_path()
log_handler = FileHandler(filename=path + '/spider163.log')
log_handler.push_application()
log = Logger("")

init(autoreset=True)


def Log(msg):
    log.warn(msg)


def Table(tb):
    print(AsciiTable(tb).table)


def Blue(msg):
    return Fore.BLUE + msg


def green(msg):
    return Fore.GREEN + msg


def red(msg):
    return Fore.RED + msg


def print_err(msg):
    print(Fore.RED + msg)


def print_warn(msg):
    print(Fore.YELLOW + msg)


def print_info(msg):
    print(Fore.BLUE + msg)
