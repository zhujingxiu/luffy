#!/usr/bin/env python
# -*- coding:utf-8 -*-
# _AUTHOR_  : zhujingxiu
# _DATE_    : 2018/1/29


import os
import logging

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HOST = '127.0.0.1'
PORT = 9999
ADDRESS = (HOST,PORT)

HOME_DIR = os.path.join(BASE_DIR,'home')

ACCOUNT_FILE = "%s/conf/accounts.ini" % BASE_DIR

LISTEN_LIMIT = 5

BUFFSIZE = 1024