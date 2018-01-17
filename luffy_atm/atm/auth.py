#!/usr/bin/env python
# -*- coding:utf-8 -*-
# _AUTHOR_  : zhujingxiu
# _DATE_    : 2018/1/15

from core import db_handler
from core import utils
from conf import settings


def authenticate(username,password):
    """
    登录认证
    :param username: 
    :param password: 
    :return: 
    """
    ret = db_handler.data_api('find', settings.USER_TABLE,
                              **{'fields': ('*',), 'where': [{'field': 'username', 'value': username}]})
    if isinstance(ret, int):
        return False
    if not len(ret):
        return False
    user = ret[0]
    if user and user.get('status') != 0:
        return False
    if utils.hash_md5(password) != user['password']:
        return False
    return user