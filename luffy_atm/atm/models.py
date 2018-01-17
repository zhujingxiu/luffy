#!/usr/bin/env python
# -*- coding:utf-8 -*-
# _AUTHOR_  : zhujingxiu
# _DATE_    : 2018/1/15

import time
from conf import settings
from core import utils
from core import db_handler
from . import transaction


def trans_auth(action):
    """
    交易认证及记录到文件
    :param action: 
    :return: 
    """

    def hook_action(*args, **kwargs):
        if not args:
            print("登录信息异常，请重新登录")
            exit(0)
        ret = action(*args, **kwargs)
        if isinstance(ret, dict):
            if 'print' not in ret or ret['print']:
                print(ret['msg'])
            if 'history' in ret:
                add_history(ret['history'])
        return False
    return hook_action


def load_user(user_id=0, username=''):
    """
    加载最新的用户信息
    :param user_id: 
    :param username: 
    :return: 
    """
    if not user_id and not username:
        return []
    field = 'username' if username else 'id'
    if user_id and username:
        field = 'id'
    value = username if field == 'username' else user_id

    ret = db_handler.data_api('find', settings.USER_TABLE,
                              **{'fields': ('*',), 'where': [{'field': field, 'value': value}]})
    if isinstance(ret, int) or not len(ret):
        return []
    return ret[0]


def profile(user, fields=''):
    """
    查看个人信息
    :param user: 指定字段
    :param fields: 指定字段
    :return: 
    """
    if not len(fields):
        fields = ('username', 'balance', 'credit', 'expire_date', 'enroll_date', 'status')
    info = {}
    new_user = load_user(user_id=user['id'])
    for i in fields:
        info[i] = new_user[i]
        if i == 'status':
            info[i] = utils.format_status(new_user['status'])
    utils.format_table(fields, [info])
    return False


def histories(user, fields=''):
    """
    查看个人信息
    :param user: 指定字段
    :param fields: 指定字段
    :return: 
    """
    if not len(fields):
        fields = ('username', 'transaction', 'amount', 'fee', 'balance', 'add_time', 'note')
    trans_logs = db_handler.data_api('find', settings.HISTORY_TABLE,
                                     **{'fields': fields, 'where': [{'field': 'user_id', 'value': user['id']}]})
    if isinstance(trans_logs, int) or not len(trans_logs):
        print('没有交易记录')
        return False
    result = []
    for item in trans_logs:
        info = {}
        for i in fields:
            info[i] = item[i]
            if i == 'add_time':
                info[i] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(item['add_time'] // 1))
            if i == 'transaction':
                info[i] = utils.format_transaction(item['transaction'])
        result.append(info)
    utils.format_table(fields, result)
    return True


@trans_auth
def repay(user, **kwargs):
    """
    还款
    :param user: 
    :param kwargs: 
    :return: 
    """
    profile(user)
    amount = input("请输入还款金额:>>").strip()
    if not amount.isdigit() and not utils.is_float_num(amount):
        print("请输入数字字符")
        return False
    amount = float(amount)
    ret = transaction.make_transaction(load_user(user_id=user['id']), 'repay', amount,
                                       **{'logger': kwargs.get('logger')})
    if not ret:
        return False
    new_user = ret.get('user', False)
    if new_user:
        history = {
            'user_id': user['id'],
            'username': user['username'],
            'transaction': 'repay',
            'amount': amount,
            'fee': ret.get('fee', 0),
            'balance': new_user['balance'],
            'add_time': time.time(),
            'note': '',
        }
        return {'status': 0, 'history': history, 'msg': '还款成功，余额 %s' % new_user['balance']}
    return False


@trans_auth
def withdraw(user, **kwargs):
    """
    取现
    :param user: 
    :param kwargs: 
    :return: 
    """
    profile(user)
    amount = input("请输入取现金额:>>").strip()
    if not amount.isdigit() and not utils.is_float_num(amount):
        print("请输入数字字符")
        return False
    amount = float(amount)
    ret = transaction.make_transaction(load_user(user_id=user['id']), 'withdraw', amount,
                                       **{'logger': kwargs.get('logger')})
    if not ret:
        return False
    new_user = ret.get('user', False)
    if new_user:
        history = {
            'user_id': user['id'],
            'username': user['username'],
            'transaction': 'withdraw',
            'amount': amount,
            'fee': ret.get('fee', 0),
            'balance': new_user['balance'],
            'add_time': time.time(),
            'note': '',
        }
        return {'status': 0, 'history': history, 'msg': '取现成功，余额 %s' % new_user['balance']}
    return False


@trans_auth
def transfer(user, **kwargs):
    """
    转账
    :param user: 
    :param kwargs: 
    :return: 
    """
    profile(user)
    username = input("请输入对方用户名:>>").strip()
    amount = input("请输入转账金额:>>").strip()
    if username == user['username']:
        print("不能转给自己")
        return False
    if not amount.isdigit() and not utils.is_float_num(amount):
        print("请输入数字字符")
        return False
    amount = float(amount)
    trans_user = load_user(username=username)
    if not trans_user:
        print("用户不存在")
        return False
    if trans_user.get('status') != 0:
        print("用户已被禁用")
        return False
    note = "转账给用户:%s" % username
    ret = transaction.make_transaction(load_user(user_id=user['id']), 'transfer', amount,
                                       **{'transfer': trans_user, 'logger': kwargs.get('logger'), 'note': note})
    if not ret:
        return False
    new_user = ret.get('user', False)
    if new_user:
        history = [
            {
                'user_id': user['id'],
                'username': user['username'],
                'transaction': 'transfer',
                'amount': amount,
                'fee': ret.get('fee', 0),
                'balance': new_user['balance'],
                'add_time': time.time(),
                'note': note,
            },
            {
                'user_id': trans_user['id'],
                'username': trans_user['username'],
                'transaction': 'transfer',
                'amount': amount,
                'fee': 0,
                'balance': float(ret.get('transfer_balance',0)) + amount,
                'add_time': time.time(),
                'note': "用户:%s转账" % user['username'],
            }
        ]
        return {'status': 0, 'history': history, 'msg': '转账成功，余额 %s' % new_user['balance']}
    return False


@utils.format_result
def update_pwd(user, **kwargs):
    """
    修改个人密码
    :param user: 
    :param kwargs: 
    :return: 
    """
    password = input("请输入新密码:>>").strip()
    confirm = input("请确认新密码:>>").strip()

    if not len(password):
        print("密码太短了")
        return False
    if password != confirm:
        print("新密码与确认密码不相符")
        return False

    db_handler.data_api('update', settings.USER_TABLE, **{'set': {'password': utils.hash_md5(password)},
                                                          'where': [{'field': 'id', 'value': user['id']}]})
    return {'status': 0, 'logger': kwargs.get('logger'), 'msg': "用户 %s 修改了密码" % user['username']}


def add_history(history):
    """
    添加交易流水记录
    :param history: 
    :return: 
    """
    records = []
    if isinstance(history, dict):
        records.append(history)
    else:
        records = history
    count_num = 0
    for item in records:

        if not set(item.keys()).issubset(settings.DATABASE['tables'][settings.HISTORY_TABLE]['structure'].keys()):
            continue
        ret = db_handler.data_api('add', settings.HISTORY_TABLE, **{'fields': item})
        if ret:
            count_num += 1
    return count_num


def go_shopping(user):
    """
    跳转到购物中心
    :param user: 
    :return: 
    """
    from mall.main import run
    new_user = load_user(user_id=user['id'])
    run(new_user)


def logout(user, **kwargs):
    """
    退出管理后台
    :return: 
    """
    msg = "用户 %s 退出ATM系统" % user['username']
    logger = kwargs.get('logger')
    if logger:
        logger.info(msg)
    print("已注销登录")
    exit(0)
