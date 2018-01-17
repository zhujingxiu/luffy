#!/usr/bin/env python
# -*- coding:utf-8 -*-
# _AUTHOR_  : zhujingxiu
# _DATE_    : 2018/1/15

import os
import logging

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# 可尝试登陆次数
LOGIN_ATTEMPTS = 3
USER_EFFECTIVE_YEARS = 5

# 日志存档目录
LOG_PATH = os.path.join(BASE_DIR, 'logs')
# 日志级别
LOG_LEVEL = logging.INFO
# 允许的日志类型
LOG_TYPES = {
    'transaction': 'transaction.log',
    'access': 'access.log',
    'admin': 'admin.log',
}
# 日志格式
LOG_FORMATTER = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# 允许的交易类型
TRANSACTION_TYPE = {
    'repay': {'title':'还款','action': 'plus', 'interest': 0},
    'withdraw': {'title':'取现','action': 'minus', 'interest': 0.05},
    'transfer': {'title':'转账','action': 'transfer', 'interest': 0.05},
    'consume': {'title':'消费','action': 'minus', 'interest': 0}
}

# 用户存档目录
USER_TABLE = 'users'
# 商品存档目录
HISTORY_TABLE = 'user_histories'
PRODUCT_TABLE = 'products'
"""
DATABASE 数据库
    engine 存储引擎 ：file_storage文件存储，mysql暂时仅生成sql语句，后期支持了直接运行生成的sql语句，返回结果集
    file_path: 仅当存储引擎为file_storage文件存储时有效。数据库目录
    tables 数据表
        file_path: 仅当存储引擎为file_storage文件存储时有效。数据表文件存储时的目录
        file_name: 仅当存储引擎为file_storage文件存储时有效。数据表文件存储时的文件名，值为structure中的字段对应的值，不可修改对应的值
        file_rule: 仅当存储引擎为file_storage文件存储时有效。数据表文件存储时的文件名的命名规则
        structure：表结构
"""
DATABASE = {
    'engine': 'file_storage',  # file_storage,support mysql in the future
    'file_path': os.path.join(BASE_DIR, 'db'),
    'tables': {
        USER_TABLE: {
            'file_path': os.path.join(BASE_DIR, 'db', USER_TABLE),
            'file_name': ('username',),
            'file_rule': 'md5',
            'structure': {
                'id': 0,
                'username': '',
                'password': '',
                'balance': 0,
                'credit': 0,
                'expire_date': '',
                'enroll_date': '',
                'status': 0,
                'cart': [],
            }
        },
        HISTORY_TABLE: {
            'file_path': os.path.join(BASE_DIR, 'db', HISTORY_TABLE),
            'file_name': ('user_id','add_time'),
            'file_rule': 'join',
            'structure': {
                'user_id': '',
                'username': '',
                'transaction': '',
                'amount': 0,
                'fee': 0,
                'balance': 0,
                'add_time': '',
                'note': '',
            }
        },
        PRODUCT_TABLE: {
            'file_path': os.path.join(BASE_DIR, 'db', PRODUCT_TABLE),
            'file_name': ('title',),
            'file_rule': 'md5',
            'structure': {
                'id': 0,
                'title': '',
                'price': 0,
                'number': 0,
                'status': 0
            }
        }
    }
}

# 前台登录后主菜单
USER_MENU = {
    '1': '进入用户中心',
    '2': '进入购物商城',
    '9': '返回上级',
    '0': '退出系统'
}
# 前台用户中心菜单
UCENTER_MENU = {
    '1': '查看我的信息',
    '2': '还款',
    '3': '取现',
    '4': '转账',
    '5': '修改密码',
    '9': '返回上级',
    '0': '退出系统'
}
# 前台购物商城菜单
MALL_MENU = {
    '1': '查看商品列表',
    '2': '查看我的购物车',
    '9': '返回上级',
    '0': '退出系统'
}

# 后台默认的管理员账户
ADMIN_ACCOUNT = 'admin'
ADMIN_PASSWORD = 'admin'
