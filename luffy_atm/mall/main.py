#!/usr/bin/env python
# -*- coding:utf-8 -*-
# _AUTHOR_  : zhujingxiu
# _DATE_    : 2018/1/17

from core import logger
from . import models

access_logger = logger.logger("access")
transaction_logger = logger.logger("transaction")


def shopping_menu():
    # 购物中心菜单
    return {
        '1': {'title': '查看商品列表', 'action': models.view_products, 'logger': transaction_logger},
        '2': {'title': '查看购物车', 'action': models.view_cart, 'logger': False},
        '3': {'title': '转到用户中心', 'action': models.go_ucenter, 'logger': False},
        '0': {'title': '退出系统', 'action': models.logout, 'logger': access_logger},
    }


def run(user):
    if user:
        dispatch(user)
    else:
        print("登录状态已过期，请重新登录")
        exit(0)


def dispatch(user):
    """
    功能分发
    :param user: 
    :return: 
    """
    menu = shopping_menu()
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

        menu[option]['action'](user, **kwargs)
        option = 0
