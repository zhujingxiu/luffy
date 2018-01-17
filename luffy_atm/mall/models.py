#!/usr/bin/env python
# -*- coding:utf-8 -*-
# _AUTHOR_  : zhujingxiu
# _DATE_    : 2018/1/16

import time
from conf import settings
from core import db_handler
from core import utils
from atm import transaction
from atm import models as atm_mod


def load_product(product_id):
    """
    加载最新的用户信息
    :param product_id: 
    :return: 
    """
    ret = db_handler.data_api('find', settings.PRODUCT_TABLE,
                              **{'fields': ('*',), 'where': [{'field': 'id', 'value': product_id}]})
    if isinstance(ret, int) or not len(ret):
        return []
    return ret[0]


def view_cart(user, fields=''):
    """
    查看购物车
    :param user: 
    :param fields: 
    :return: 
    """
    if not fields:
        fields = ('title', 'amount', 'created_at')
    if 'cart' not in user or not len(user['cart']):
        print('没有购买记录')
        return False

    result = []
    for item in user['cart']:
        tmp = {}
        for field in fields:
            tmp[field] = item[field]
        result.append(tmp)

    utils.format_table(fields, result)
    return False


def view_products(user, **kwargs):
    """
    查看商品列表
    :param user: 
    :param kwargs: 
    :return: 
    """
    fields = kwargs.get('fields', ())
    if not len(fields):
        fields = ('id', 'title', 'price', 'number', 'status')

    ret = db_handler.data_api('find', settings.PRODUCT_TABLE,
                              **{'fields': fields, 'where': [{'field': 'status', 'logic': '!=', 'value': 1}]})
    if isinstance(ret, int):
        return ret
    if not len(ret):
        print('没有商品')
        return False
    result = []
    for i in ret:
        if 'status' in i:
            i.update({'status': utils.format_status(i['status'])})
        result.append(i)
    utils.format_table(fields, result)

    option = input("请输入要购买的商品ID，（0，注销;b，返回）:>>").strip()
    if option.isdigit():
        if option == '0':
            logout(user, **kwargs)
        else:
            consume(user, **{'product_id': int(option), 'logger': kwargs.get('logger')})
    elif option.lower() == 'b':
        return True


@atm_mod.trans_auth
def consume(user, **kwargs):
    """
    消费
    :param user: 
    :param kwargs: 
    :return: 
    """
    product_id = kwargs.get('product_id')
    if not product_id:
        print('商品参数异常')
        return False

    product = load_product(product_id)
    if not product or product['status'] != 0 or product['number'] == 0:
        print("商品状态异常，无存货或已下架")
        return False
    amount = float(product['price'])
    kwargs['note'] = "购买商品：%s" % product['title']
    ret = transaction.make_transaction(user, 'consume', amount, **kwargs)
    if not ret:
        return False
    new_user = ret.get('user',False)
    if new_user:
        ret1 = add_cart(user, product)
        new_number = product['number'] - 1
        update = {
            'number': new_number
        }
        if not update['number']:
            update['status'] = 1
        ret3 = db_handler.data_api('update', settings.PRODUCT_TABLE,
                                   **{'set': update, 'where': [{'field': 'id', 'value': product_id}]})
        history = {
            'user_id': user['id'],
            'username': user['username'],
            'transaction': 'consume',
            'amount': amount,
            'fee': ret.get('fee',0),
            'balance': new_user['balance'],
            'add_time': time.time(),
            'note': kwargs['note'],
        }
        return {'status': 0, 'history': history, 'msg': '购买成功，余额 %s' % new_user['balance']}
    return False


def add_cart(user, product):
    """
    添加商品到用户购物车
    :param user: 
    :param product: 
    :return: 
    """
    user['cart'].append({
        'product_id': product['id'],
        'title': product['title'],
        'amount': product['price'],
        'number': 1,
        'created_at': utils.calculate_date(time_format=True)
    })
    return db_handler.data_api('update', settings.USER_TABLE,
                               **{'set': {'cart': user['cart']}, 'where': [{'field': 'id', 'value': user['id']}]})


def go_ucenter(user):
    """
    跳转到用户中心
    :param user: 
    :return: 
    """
    from atm.main import run
    new_user = atm_mod.load_user(user_id=user['id'])
    run(new_user)


def logout(user, **kwargs):
    """
    退出管理后台
    :return: 
    """
    atm_mod.logout(user, **kwargs)
