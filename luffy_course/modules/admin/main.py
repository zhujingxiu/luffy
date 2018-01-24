#!/usr/bin/env python
# -*- coding:utf-8 -*-
# _AUTHOR_  : zhujingxiu
# _DATE_    : 2018/1/22

from modules.service import Service
from conf import settings
from core.logger import Logger
from .models import Models
from .auth import Auth


class Main(Service):
    __log_type__ = 'admin'
    __admin_menu__ = {
        '1': {'title': '查看学校列表', 'action': Models.show_schools, 'log': False},
        '2': {'title': '添加学校信息', 'action': Models.create_school, 'log': True},
        '3': {'title': '修改学校信息', 'action': Models.update_school, 'log': True},

        '4': {'title': '查看讲师列表', 'action': Models.show_teachers, 'log': False},
        '5': {'title': '添加讲师信息', 'action': Models.create_teacher, 'log': True},
        '6': {'title': '修改讲师信息', 'action': Models.update_teacher, 'log': True},

        '7': {'title': '查看课程列表', 'action': Models.show_courses, 'log': False},
        '8': {'title': '添加课程信息', 'action': Models.create_course, 'log': True},
        '9': {'title': '修改课程信息', 'action': Models.update_course, 'log': True},

        '10': {'title': '查看班级列表', 'action': Models.show_classes, 'log': False},
        '11': {'title': '添加班级信息', 'action': Models.create_class, 'log': True},
        '12': {'title': '修改班级信息', 'action': Models.update_class, 'log': True},

        '0': {'title': '退出系统', 'action': Auth.logout, 'log': True},
    }

    @classmethod
    def run(cls):
        admin_authenticate = False
        retry_count = 0
        while retry_count < settings.LOGIN_ATTEMPTS:
            username = input("请输入管理员账号:>>").strip()
            password = input("请输入管理员密码:>>").strip()
            if Auth.authenticate(**{'username': username, 'password': password, 'logger': Logger(cls.__log_type__)}):
                print('\033[92m登录成功\033[0m')
                admin_authenticate = True
                break
            else:
                print('登录失败，用户名和密码不匹配')
                retry_count += 1
        else:
            print('输入错误次数太多，已强制退出')
            exit(0)

        if admin_authenticate:
            cls.interactive(None)

    @classmethod
    def interactive(cls,user):
        option = 0
        menu = cls.__admin_menu__
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
            menu[option]['action'](**kwargs)
            option = 0
