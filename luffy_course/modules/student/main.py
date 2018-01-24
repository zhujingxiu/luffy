#!/usr/bin/env python
# -*- coding:utf-8 -*-
# _AUTHOR_  : zhujingxiu
# _DATE_    : 2018/1/22
from modules.service import Service
from core.logger import Logger
from .models import Models
from .auth import Auth


class Main(Service):
    __log_type = 'student'
    __main_menu = {
        '1': {'title': '注册', 'action': Auth.regist, 'log': True},
        '2': {'title': '登录', 'action': Auth.login, 'log': True},
    }
    __student_menu = {
        '1': {'title': '查看信息', 'action': Models.profile, 'log': False},
        '2': {'title': '充值', 'action': Models.recharge, 'log': True},
        '3': {'title': '查看班级', 'action': Models.show_classes, 'log': True},
        '4': {'title': '查看成绩', 'action': Models.show_scores, 'log': False},
        '5': {'title': '查看交易记录', 'action': Models.show_transactions, 'log': False},

        '0': {'title': '退出系统', 'action': Auth.logout, 'log': True},
    }

    @classmethod
    def run(cls):
        while True:
            menu = cls.__main_menu
            for k in menu:
                print("%s.%s" % (k, menu[k]['title']))
            option = input("请输入操作序号:>>").strip()
            if option not in menu.keys():
                print("错误的选项")
                continue
            ret = menu[option]['action'](**{'logger': Logger(cls.__log_type)})

            if ret:
                from libs.luffy_student import LuffyStudent
                if isinstance(ret, LuffyStudent):
                    cls.interactive(ret)

    @classmethod
    def interactive(cls, user):
        option = 0
        menu = cls.__student_menu
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
                kwargs['logger'] = Logger(cls.__log_type)
            menu[option]['action'](user, **kwargs)
            option = 0
