#!/usr/bin/env python
# -*- coding:utf-8 -*-
# _AUTHOR_  : zhujingxiu
# _DATE_    : 2018/1/15

from conf import settings
from core import logger
from .auth import authenticate
from . import models
import os

access_logger = logger.logger("access")
transaction_logger = logger.logger("transaction")


def atm_menu():
    # 用户中心菜单
    return {
        '1': {'title': '查看个人信息', 'action': models.profile, 'logger': False},
        '2': {'title': '还款', 'action': models.repay, 'logger': transaction_logger},
        '3': {'title': '取现', 'action': models.withdraw, 'logger': transaction_logger},
        '4': {'title': '转账', 'action': models.transfer, 'logger': transaction_logger},
        '5': {'title': '转到购物商城', 'action': models.go_shopping, 'logger': False},
        '0': {'title': '退出系统', 'action': models.logout, 'logger': access_logger},
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
    ATM交互入口
    :return: 
    """
    initial()
    user_authenticate = False
    user = {}
    retry_count = 0
    while retry_count < settings.LOGIN_ATTEMPTS:
        username = input("请输入账号:>>").strip()
        password = input("请输入密码:>>").strip()
        ret = authenticate(username, password)
        if ret:
            print('登录成功')
            access_logger.info("用户%s登录成功" % username)
            user_authenticate = True
            user = ret
            break
        else:
            print('登录失败，用户名和密码不匹配')
            retry_count += 1
    else:
        print('输入错误次数太多，已强制退出')
        exit(0)

    if user_authenticate:
        dispatch(user)


def dispatch(user):
    """
    功能分发
    :param option: 
    :return: 
    """
    menu = atm_menu()
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
        if menu[option]['logger']:
            kwargs['logger'] = menu[option]['logger']

        ret = menu[option]['action'](user,**kwargs)

        option = 0
