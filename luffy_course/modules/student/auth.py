#!/usr/bin/env python
# -*- coding:utf-8 -*-
# _AUTHOR_  : zhujingxiu
# _DATE_    : 2018/1/15

from conf import settings
from core import utils
from libs.luffy_student import LuffyStudent
from libs.luffy_school import LuffySchool


class Auth:
    @staticmethod
    def login(**kwargs):
        """
        登录
        :param kwargs:
        :return: 
        """
        retry_count = 0
        while retry_count < settings.LOGIN_ATTEMPTS:
            username = input("请输入用户名:>>").strip()
            password = input("请输入密码:>>").strip()
            ret = Auth.authenticate(**{'username': username, 'password': password, 'logger': kwargs.get('logger')})
            if ret:
                print('\033[92m登录成功\033[0m')
                return ret
            else:
                print('登录失败，用户名和密码不匹配')
                retry_count += 1
        else:
            print('输入错误次数太多，已强制退出')
            exit(0)

    @staticmethod
    def regist(**kwargs):
        """
        学生注册
        :param kwargs:  
        :return: 
        """
        username = input("请输入用户名（b,返回）：>>").strip()
        if username.lower() == 'b':
            return False
        password = input("请输入登录密码：>>").strip()
        if not len(password):
            print('密码不得为空')
            return False
        schools = LuffySchool.fetch_all()
        print("学校列表")
        if not len(schools):
            print("没有找到学校")
            return []
        for i, entry in enumerate(schools, 1):
            print('# ', i, entry)
        entry_id = input("请输入所属学校序号：>>").strip()
        index = int(entry_id) - 1
        if index < 0 or index >= len(schools):
            print("错误的选项")
            return False
        entry = LuffyStudent(username, password, schools[index].sn)
        entry.save()
        logger = kwargs.get('logger')
        if logger:
            logger.log("用户 %s 注册成功" % username)
        print("注册成功")
        return True

    @staticmethod
    def authenticate(**kwargs):
        """
        登录认证
        :param kwargs: 
        :return: 
        """
        username = kwargs.get('username')
        password = kwargs.get('password')
        records = LuffyStudent.fetch_all()
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
                logger.log("学生%s登录系统" % username)
            return student
        return False

    @staticmethod
    def logout(user, **kwargs):

        logger = kwargs.get('logger')
        if logger:
            logger.log("学生%s登出系统" % user.username)

        print("已注销登录")
        exit(0)
