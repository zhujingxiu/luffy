#!/usr/bin/env python
# -*- coding:utf-8 -*-
# _AUTHOR_  : zhujingxiu
# _DATE_    : 2018/1/15

from conf import settings
from core import db_handler


def make_transaction(user, tran_type, amount, **kwargs):
    """
    账户交易中心
    :param user: 
    :param tran_type: 
    :param amount: 
    :param kwargs: 
    :return: 
    """
    if not user:
        print("用户信息异常" % tran_type)
        return False
    amount = float(amount)
    if tran_type not in settings.TRANSACTION_TYPE:
        print("不支持的交易类型 %s " % tran_type)
        return False

    fee = amount * settings.TRANSACTION_TYPE[tran_type]['interest']
    old_balance = user['balance']
    if settings.TRANSACTION_TYPE[tran_type]['action'] == 'plus':
        new_balance = old_balance + amount + fee
    elif settings.TRANSACTION_TYPE[tran_type]['action'] == 'minus':
        new_balance = old_balance - amount - fee
        if new_balance < 0:
            print("\033[91m交易失败：\033[0m用户额度[%s]，不足以支付本次交易金额（含手续费[-%s], 当前用户余额[%s]" % (user['credit'], (amount + fee), old_balance))
            return

    db_handler.data_api('update', settings.USER_TABLE, **{'set': {'balance': new_balance}, 'where': [
        {'field': 'id', 'value': user['id']}]})
    log_obj = kwargs.get('logger')
    log_obj.info("账户:%s   操作:%s    金额:%s   手续费:%s" % (user['id'], tran_type, amount, fee))
    return user
