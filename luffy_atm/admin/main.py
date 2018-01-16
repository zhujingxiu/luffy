#!/usr/bin/env python
# -*- coding:utf-8 -*-
# _AUTHOR_  : zhujingxiu
# _DATE_    : 2018/1/15

from conf import settings
from core import logger
from .auth import authenticate
from . import models
import os

admin_logger = logger.logger("admin")


def admin_menu():
    # 后台管理菜单
    return {
        '1': {'title': '查看用户列表', 'action': models.view_users, 'log': False},
        '2': {'title': '添加用户信息', 'action': models.add_user, 'log': True},
        '3': {'title': '修改用户额度', 'action': models.update_user, 'log': True},
        '4': {'title': '禁用用户状态', 'action': models.deactivate_user, 'log': True},
        '5': {'title': '查看商品列表', 'action': models.view_products, 'log': False},
        '6': {'title': '添加商品信息', 'action': models.add_product, 'log': True},
        '7': {'title': '修改商品信息', 'action': models.update_product, 'log': True},
        '8': {'title': '下架商品', 'action': models.deactivate_product, 'log': True},
        '0': {'title': '退出系统', 'action': models.logout, 'log': False},
    }


def initial():
    """
    初始化目录
    :return: 
    """
    if not os.path.exists(settings.LOG_PATH):
        os.mkdir(settings.LOG_PATH)

    if settings.DATABASE['engine'] == 'file_storage':
        if not os.path.exists(settings.DATABASE['file_path']):
            os.mkdir(settings.DATABASE['file_path'])
        for table in settings.DATABASE['tables']:
            if not os.path.exists(settings.DATABASE['tables'][table]['file_path']):
                os.mkdir(settings.DATABASE['tables'][table]['file_path'])


def run():
    """
    管理后台交互入口
    :return: 
    """
    initial()
    admin_authenticate = False
    retry_count = 0
    while retry_count < settings.LOGIN_ATTEMPTS:
        username = input("请输入管理员账号:>>").strip()
        password = input("请输入管理员密码:>>").strip()

        if authenticate(username, password):
            print('登录成功')
            admin_authenticate = True
            break
        else:
            print('登录失败，用户名和密码不匹配')
            retry_count += 1
    else:
        print('输入错误次数太多，已强制退出')
        exit(0)

    if admin_authenticate:

        dispatch()


def dispatch():
    """
    功能分发
    :param option: 
    :return: 
    """
    menu = admin_menu()
    option = 0
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
            kwargs['logger'] = admin_logger

        ret = menu[option]['action'](**kwargs)

        option = 0
