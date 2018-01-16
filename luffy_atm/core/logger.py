#!/usr/bin/env python
# -*- coding:utf-8 -*-
# _AUTHOR_  : zhujingxiu
# _DATE_    : 2018/1/15

import os
import logging
from conf import settings


def logger(log_type):
    """
    创建logger
    :param log_type: 记录类型
    :return: 
    """
    logger = logging.getLogger(log_type)
    logger.setLevel(settings.LOG_LEVEL)

    # create file handler and set level to warning
    log_file = os.path.join(settings.LOG_PATH, settings.LOG_TYPES[log_type])

    fh = logging.FileHandler(log_file, encoding='UTF-8')
    fh.setLevel(settings.LOG_LEVEL)
    # create formatter
    formatter = settings.LOG_FORMATTER

    fh.setFormatter(formatter)

    logger.addHandler(fh)

    return logger
