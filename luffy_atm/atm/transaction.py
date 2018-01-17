#!/usr/bin/env python
# -*- coding:utf-8 -*-
# _AUTHOR_  : zhujingxiu
# _DATE_    : 2018/1/15

from conf import settings
from core import db_handler


def make_transaction(user, trans_type, amount, **kwargs):
    """
    账户交易中心
    :param user: 
    :param trans_type: 
    :param amount: 
    :param kwargs: 
    :return: 
    """
    if not user:
        print("用户信息异常" % trans_type)
        return False
    amount = float(amount)
    if trans_type not in settings.TRANSACTION_TYPE:
        print("不支持的交易类型 %s " % trans_type)
        return False
    new_balance = 0
    transfer_balance = 0
    # 手续费
    fee = amount * settings.TRANSACTION_TYPE[trans_type]['interest']
    if settings.TRANSACTION_TYPE[trans_type]['action'] == 'plus':
        new_balance = user['balance'] + amount + fee
    elif settings.TRANSACTION_TYPE[trans_type]['action'] in ('minus', 'transfer'):
        new_balance = user['balance'] - amount - fee
        if new_balance < 0:
            print("\033[91m交易失败：\033[0m用户额度[%s]，不足以支付本次交易金额[-%s]（含手续费）, 当前用户余额[%s]" % (
                user['credit'], (amount + fee), user['balance']))
            return False
        transfer = kwargs.get('transfer', False)
        if transfer:
            transfer_balance = transfer['balance'] + amount
            db_handler.data_api('update', settings.USER_TABLE, **{'set': {'balance': transfer_balance},
                                                                  'where': [{'field': 'id', 'value': transfer['id']}]})

    db_handler.data_api('update', settings.USER_TABLE,
                        **{'set': {'balance': new_balance}, 'where': [{'field': 'id', 'value': user['id']}]})
    user['balance'] = new_balance
    log_obj = kwargs.get('logger')
    if log_obj:
        log_obj.info(
            "账户:%s 操作:%s 金额:%s 手续费:%s 备注:%s" % (user['username'], trans_type, amount, fee, kwargs.get('note', '')))
    return {'user': user, 'fee': fee, 'transfer_balance': transfer_balance}
