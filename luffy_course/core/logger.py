#!/usr/bin/env python
# -*- coding:utf-8 -*-
# _AUTHOR_  : zhujingxiu
# _DATE_    : 2018/1/15

import os
import logging
from conf import settings


class Logger:
    def __init__(self, log_type):
        """
        创建logger
        :param log_type: 记录类型
        :return: 
        """
        self.logger = logging.getLogger(log_type)
        self.logger.setLevel(settings.LOG_LEVEL)

        log_file = os.path.join(settings.LOG_PATH, settings.LOG_TYPES[log_type])

        fh = logging.FileHandler(log_file, encoding='UTF-8')
        fh.setLevel(settings.LOG_LEVEL)
        fh.setFormatter(settings.LOG_FORMATTER)

        self.logger.addHandler(fh)

    def log(self, msg):
        """
        封装记录方法
        :param msg: 
        :return: 
        """
        self.logger.info(msg)
