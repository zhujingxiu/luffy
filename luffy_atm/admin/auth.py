#!/usr/bin/env python
# -*- coding:utf-8 -*-
# _AUTHOR_  : zhujingxiu
# _DATE_    : 2018/1/15

from conf import settings


def authenticate(username,password):
    """
    登录认证
    :param username: 
    :param password: 
    :return: 
    """
    if username == settings.ADMIN_ACCOUNT and password == settings.ADMIN_PASSWORD:
        return True
    return False
