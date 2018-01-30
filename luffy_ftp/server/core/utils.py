#!/usr/bin/env python
# -*- coding:utf-8 -*-
# _AUTHOR_  : zhujingxiu
# _DATE_    : 2018/1/22


def hash_md5(content):
    """
    md5文本加密
    :param content: 
    :return: 
    """
    import hashlib
    encrypt = hashlib.md5()
    encrypt.update(bytes(content, encoding='utf-8'))
    return encrypt.hexdigest()


def calculate_date(years=0, months=0, days=0, time_format=False):
    """
    日期加减
    :param years: 
    :param months: 
    :param days: 
    :param time_format: 
    :return: 
    """
    import datetime
    date_formatter = "%Y-%m-%d"
    if time_format:
        date_formatter = "%Y-%m-%d %H:%M:%S"
    dt = datetime.datetime.now()
    return dt.replace(year=dt.year + years, month=dt.month + months, day=dt.day + days).strftime(date_formatter)


def is_float_num(string):
    """
    正则判断浮点字符
    :param string: 
    :return: 
    """
    import re
    ret = re.search('^-?([1-9]\d*\.\d*|0\.\d*[1-9]\d*|0?\.0+|0)$', string)
    return ret


def format_filesize(string):
    """
    格式化数据大小
    :param string: 
    :return: 
    """
    import re
    ret = re.search('(\d+)(\w)?',string)
    if not ret.group(2):
        unit = 'm'
    else:
        unit = ret.group(2).lower()
    if unit not in ('k','kb','m','mb','g','gb'):
        unit = 'm'
    if unit in ('k','kb'):
        return int(ret.group(1))*1024
    if unit in ('m','mb'):
        return int(ret.group(1))*1024*1024
    if unit in ('g','gb'):
        return int(ret.group(1)) * 1024*1024*1024


def dir_used(path):
    """
    统计目录大小
    :param path: 
    :return: 
    """
    import os
    used_size = 0
    for root, dirs, files in os.walk(path, topdown=False):
        for name in files:
            used_size += os.path.getsize(os.path.join(root, name))

    return used_size


def file_md5(filepath):
    """
    文件MD5校验值
    :param filepath: 
    :return: 
    """
    import hashlib
    encrypt = hashlib.md5()
    with open(filepath, 'rb') as f:
        while True:
            b = f.read(8096)
            if not b:
                break
            encrypt.update(b)
    return encrypt.hexdigest()
