#!/usr/bin/env python
# -*- coding:utf-8 -*-
# _AUTHOR_  : zhujingxiu
# _DATE_    : 2018/1/29

import os


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

LOGIN_ATTEMPTS = 3
ADDRESS = ('localhost', 9999)

BUFFSIZE = 1024

DOWNLOAD_DIR = '%s/download/' % BASE_DIR
