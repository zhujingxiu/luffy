#!/usr/bin/env python
# -*- coding:utf-8 -*-
# _AUTHOR_  : zhujingxiu
# _DATE_    : 2018/1/15

from conf import settings


class Auth:
    @staticmethod
    def authenticate(**kwargs):
        """
        登录认证
        :param username: 
        :param password: 
        :return: 
        """
        username = kwargs.get('username')
        password = kwargs.get('password')
        if username == settings.ADMIN_ACCOUNT and password == settings.ADMIN_PASSWORD:
            logger = kwargs.get('logger')
            if logger:
                logger.log("管理员%s登录系统" % username)
            return True
        return False

    @staticmethod
    def logout(**kwargs):

        logger = kwargs.get('logger')
        if logger:
            logger.log("管理员登出系统")

        print("已注销登录")
        exit(0)
