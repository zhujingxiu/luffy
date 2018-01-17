#!/usr/bin/env python
# -*- coding:utf-8 -*-
# _AUTHOR_  : zhujingxiu
# _DATE_    : 2018/1/15


from conf import settings
from core import db_handler
from core import utils
import os


def format_result(action):
    """
    处理操作结果
    :param action: 
    :return: 
    """

    def hook_action(**kwargs):
        ret = action(**kwargs)
        if isinstance(ret, dict):
            status = ret.get('status', 0)
            if status < 0:
                print(ret['status'])
                return False
            logger = ret.get('logger', False)
            if logger:
                logger.info(ret['msg'])
                print("\033[92m操作成功,\033[0m操作内容：%s" % ret['msg'])
                return True
        return False

    return hook_action


def view_users(fields=''):
    """
    查看用户列表
    :param fields: 指定字段
    :return: 
    """
    if not len(fields):
        fields = ('id', 'username', 'balance', 'credit', 'expire_date', 'enroll_date', 'status')
    ret = db_handler.data_api('find', settings.USER_TABLE, **{'fields': fields})
    if isinstance(ret, int):
        return ret
    if not len(ret):
        print('没有结果')
        return False
    result = []
    for i in ret:
        if 'status' in i:
            i.update({'status': utils.format_status(i['status'])})
        result.append(i)
    utils.format_table(fields, result)
    return ret


@utils.format_result
def add_user(**kwargs):
    """
    添加用户
    :param kwargs: 
    :return: 
    """
    username = input("请输入用户名，（b,返回）:>>").strip()
    if username.lower() == 'b':
        return False
    password = input("请输入用户密码:>>").strip()
    credit = input("请输入用户额度:>>").strip()

    if check_exists(settings.USER_TABLE, **{'where': [{'field': 'username', 'value': username}]}):
        print("用户已存在")
        return False
    if not credit.isdigit() and not utils.is_float_num(credit):
        print("请输入数字字符")
        return False
    entry = settings.DATABASE['tables'][settings.USER_TABLE]['structure']
    entry.update({
        'id': get_increment_id(settings.USER_TABLE),
        'username': username,
        'password': utils.hash_md5(password),
        'credit': float(credit),
        'balance': float(credit),
        'enroll_date': utils.calculate_date(),
        'expire_date': utils.calculate_date(years=settings.USER_EFFECTIVE_YEARS),
    })
    ret = db_handler.data_api('add', settings.USER_TABLE, **{'fields': entry})
    if ret:
        return {'status': ret, 'logger': kwargs.get('logger'), 'msg': "管理员添加用户 %s" % username}
    return False


def get_increment_id(table):
    """
    取自增ID
    :param table: 
    :return: 
    """
    records = db_handler.fetch_all(table)
    if not len(records):
        return 1
    ids = [0]
    for record in records:
        ids.append(int(record['id']))
    return max(ids) + 1


def check_exists(table, **kwargs):
    """
    验证是否存在记录
    :param table: 
    :param kwargs: 
    :return: 
    """
    ret = db_handler.data_api('find', table, **{'fields': ('*',), 'where': kwargs.get('where')})

    return False if isinstance(ret, int) else len(ret)


@utils.format_result
def update_user(**kwargs):
    """
    编辑用户信息
    :param kwargs: 
    :return: 
    """
    records = view_users()
    if not records:
        print('没有找到结果')
        return False
    entry_id = input("请输入用户ID，（b,返回）:>>").strip()
    if entry_id.lower() == 'b':
        return False
    credit = input("请重新输入用户额度:>>").strip()
    if not credit.isdigit() and not utils.is_float_num(credit):
        print("请输入数字字符")
        return False
    ret = db_handler.data_api('update', settings.USER_TABLE,
                              **{'set': {'credit': float(credit)}, 'where': [{'field': 'id', 'value': int(entry_id)}]})
    if ret:
        return {'status': ret, 'logger': kwargs.get('logger'), 'msg': "管理员修改用户ID: %s 的额度" % entry_id}
    return False


@utils.format_result
def deactivate_user(**kwargs):
    """
    禁用用户状态
    :param kwargs: 
    :return: 
    """
    records = view_users()
    if not records:
        print('没有找到结果')
        return False
    entry_id = input("请输入用户ID，（b,返回）:>>").strip()
    if entry_id.lower() == 'b':
        return False
    ret = db_handler.data_api('update', settings.USER_TABLE,
                              **{'set': {'status': 1}, 'where': [{'field': 'id', 'value': int(entry_id)}]})
    if ret:
        return {'status': ret, 'logger': kwargs.get('logger'), 'msg': "管理员修改了用户ID %s 为禁用状态" % entry_id}
    return False


def view_products(fields=''):
    """
    查看商品列表
    :param fields: 
    :return: 
    """
    if not len(fields):
        fields = ('id', 'title', 'price', 'number', 'status')
    ret = db_handler.data_api('find', settings.PRODUCT_TABLE, **{'fields': fields})
    if isinstance(ret, int):
        return ret
    if not len(ret):
        return False
    result = []
    for i in ret:
        if 'status' in i:
            i.update({'status': utils.format_status(i['status'])})
        result.append(i)
    utils.format_table(fields, result)
    return ret


@utils.format_result
def update_product(**kwargs):
    """
    编辑商品信息
    :param kwargs: 
    :return: 
    """
    records = view_products()
    if not records:
        print('没有找到结果')
        return False
    entry_id = input("请输入商品ID，（b,返回）:>>").strip()
    if entry_id.lower() == 'b':
        return False
    price = input("请重新输入单价:>>").strip()
    number = input("请重新输入数量:>>").strip()
    if not price.isdigit() or not number.isdigit():
        print("请输入数字字符")
        return False
    ret = db_handler.data_api('update', settings.PRODUCT_TABLE,
                              **{'set': {'price': float(price), 'number': int(number)},
                                 'where': [{'field': 'id', 'value': int(entry_id)}]})
    if ret:
        return {'status': ret, 'logger': kwargs.get('logger'), 'msg': "管理员修改了商品ID: %s 的信息" % entry_id}
    return False


@utils.format_result
def add_product(**kwargs):
    """
    添加商品信息
    :param kwargs: 
    :return: 
    """
    title = input("请输入商品名，（b,返回）:>>").strip()
    if title.lower() == 'b':
        return False
    price = input("请输入单价:>>").strip()
    number = input("请输入数量:>>").strip()

    if check_exists(settings.PRODUCT_TABLE, **{'where': [{'field': 'title', 'value': title}]}):
        print("商品%s已存在" % title)
        return False
    if not price.isdigit() and not utils.is_float_num(price):
        print("请输入数字字符")
        return False
    if not number.isdigit():
        print("请输入数字字符")
        return False
    entry = settings.DATABASE['tables'][settings.PRODUCT_TABLE]['structure']
    entry.update({
        'id': get_increment_id(settings.PRODUCT_TABLE),
        'title': title,
        'price': float(price),
        'number': int(number),
    })
    ret = db_handler.data_api('add', settings.PRODUCT_TABLE, **{'fields': entry})
    if ret:
        return {'status': ret, 'logger': kwargs.get('logger'), 'msg': "管理员添加商品 %s" % title}
    return False


@utils.format_result
def deactivate_product(**kwargs):
    """
    商品下架
    :param kwargs: 
    :return: 
    """
    records = view_products()
    if not records:
        print('没有找到结果')
        return False
    entry_id = input("请输入商品ID，（b,返回）::>>").strip()
    if entry_id.lower() == 'b':
        return False
    ret = db_handler.data_api('update', settings.PRODUCT_TABLE,
                              **{'set': {'status': 1}, 'where': [{'field': 'id', 'value': int(entry_id)}]})
    if ret:
        return {'status': ret, 'logger': kwargs.get('logger'), 'msg': "管理员修改了商品ID %s 为下架状态" % entry_id}
    return False


def logout():
    """
    退出管理后台
    :return: 
    """
    print("退出管理后台")
    exit(0)
