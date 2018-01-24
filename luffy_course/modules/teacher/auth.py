#!/usr/bin/env python
# -*- coding:utf-8 -*-
# _AUTHOR_  : zhujingxiu
# _DATE_    : 2018/1/15

from core import utils
from libs.luffy_teacher import LuffyTeacher


class Auth:

    @staticmethod
    def authenticate(**kwargs):
        """
        登录认证
        :param kwargs: 
        :return: 
        """
        username = kwargs.get('username')
        password = kwargs.get('password')
        records = LuffyTeacher.fetch_all()
        if not len(records):
            return False
        student = None
        for entry in records:
            if entry.username == username and utils.hash_md5(password):
                student = entry
                break
        if student:
            logger = kwargs.get('logger')
            if logger:
                logger.log("讲师%s登录系统" % username)
            return student
        return False

    @staticmethod
    def logout(user, **kwargs):

        logger = kwargs.get('logger')
        if logger:
            logger.log("讲师%s登出系统" % user.username)

        print("已注销登录")
        exit(0)
