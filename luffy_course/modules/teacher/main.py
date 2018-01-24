#!/usr/bin/env python
# -*- coding:utf-8 -*-
# _AUTHOR_  : zhujingxiu
# _DATE_    : 2018/1/22

from conf import settings
from core.logger import Logger
from .models import Models
from .auth import Auth


class Main:
    __log_type__ = 'teacher'

    __teacher_menu__ = {
        '1': {'title': '查看个人信息', 'action': Models.profile, 'log': False},
        '2': {'title': '查看班级', 'action': Models.show_classes, 'log': True},
        '3': {'title': '查看学生', 'action': Models.show_students, 'log': False},
        '4': {'title': '查看上课记录', 'action': Models.show_duties, 'log': False},

        '0': {'title': '退出系统', 'action': Auth.logout, 'log': True},
    }

    @classmethod
    def run(cls):
        teacher = None
        retry_count = 0
        while retry_count < settings.LOGIN_ATTEMPTS:
            username = input("请输入讲师账户:>>").strip()
            password = input("请输入登录密码:>>").strip()
            ret = Auth.authenticate(**{'username': username, 'password': password, 'logger': Logger(cls.__log_type__)})
            if ret:
                print('\033[92m登录成功\033[0m')
                teacher = ret
                break
            else:
                print('登录失败，用户名和密码不匹配')
                retry_count += 1
        else:
            print('输入错误次数太多，已强制退出')
            exit(0)

        if teacher:
            cls.interactive(teacher)

    @classmethod
    def interactive(cls, user):
        option = 0
        menu = cls.__teacher_menu__
        while not option:
            for k in menu:
                print("%s.%s" % (k, menu[k]['title']))
            option = input("请输入操作序号:>>").strip()
            if option not in menu.keys():
                option = 0
                print("错误的选项")
                continue
            kwargs = {}
            if menu[option]['log']:
                kwargs['logger'] = Logger(cls.__log_type__)
            menu[option]['action'](user, **kwargs)
            option = 0
