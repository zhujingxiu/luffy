#!/usr/bin/env python
# -*- coding:utf-8 -*-
# _AUTHOR_  : zhujingxiu
# _DATE_    : 2018/1/4
import os
import hashlib
import json
import time

"""
作业题目: 购物车程序

基础要求：
1、启动程序后，输入用户名密码后，让用户输入工资，然后打印商品列表
2、允许用户根据商品编号购买商品
3、用户选择商品后，检测余额是否够，够就直接扣款，不够就提醒
4、可随时退出，退出时，打印已购买商品和余额
5、在用户使用过程中， 关键输出，如余额，商品已加入购物车等消息，需高亮显示

扩展需求：
1、用户下一次登录后，输入用户名密码，直接回到上次的状态，即上次消费的余额什么的还是那些，再次登录可继续购买
2、允许查询之前的消费记录
"""
# 高亮
HL_OKBLUE = '\033[94m'
HL_OKGREEN = '\033[92m'
HL_FAIL = '\033[91m'
HL_ENDC = '\033[0m'
# 出错消息
ERROR_NO_RESULT = HL_FAIL + '没有记录' + HL_ENDC
ERROR_EMPTY_CART = HL_FAIL + '您的购物车空空如也' + HL_ENDC
ERROR_NO_GOODS = HL_FAIL + '没有该商品' + HL_ENDC
ERROR_USER_INPUT = HL_FAIL + '输入不合法' + HL_ENDC
ERROR_USER_PASSWORD = HL_FAIL + '用户名密码不匹配' + HL_ENDC
ERROR_USER_LOGIN = HL_FAIL + '用户已登出，请重新登录' + HL_ENDC
ERROR_USER_EXISTS = HL_FAIL + '用户已存在' + HL_ENDC
ERROR_USER_NOT_EXISTS = HL_FAIL + '用户不存在' + HL_ENDC
ERROR_USER_BALANCE = HL_FAIL + '用户余额不足' + HL_ENDC
# 成功消息
SUCCESS_USER_HALT = HL_OKBLUE + '退出系统' + HL_ENDC
SUCCESS_USER_ADDED = HL_OKGREEN + '用户注册成功,您将进入到用户中心' + HL_ENDC
SUCCESS_USER_LOGIN = HL_OKGREEN + '用户登录成功' + HL_ENDC
SUCCESS_USER_RECHARGE = HL_OKGREEN + '用户充值成功' + HL_ENDC
SUCCESS_USER_REPASSWD = HL_OKGREEN + '用户密码修改成功' + HL_ENDC
SUCCESS_USER_PURCHASED = HL_OKGREEN + '购买成功，商品已加入购物车' + HL_ENDC
# 用户存档目录
users_dir = 'module01_users'
if not os.path.exists(users_dir):
    os.mkdir(users_dir)
# 商品列表
goods = [
    {"name": "电脑", "price": 1999},
    {"name": "鼠标", "price": 10},
    {"name": "游艇", "price": 20},
    {"name": "美女", "price": 998},
    {"name": "机器人", "price": 2998},
    {"name": "特斯拉", "price": 5998}
]
products = []
for i, product in enumerate(goods, 100):
    products.append("%d. %s\t %.2f" % (i, product['name'], product['price']))
goods_menu = """
------------商品列表----------
序号 名称\t 价格
%s
-----------------------------
999. 返回上级
  0. 退出系统
""" % os.linesep.join(products)

# 用户中心面板
user_menu = """
------------用户中心----------
11. 购买商品
12. 查看购物车
13. 查看账户流水
14. 账户充值
15. 修改密码
0. 退出系统
-----------------------------
"""
# 主操作面板
main_menu = """
------------操作面板----------
1. 登录商城
2. 注册用户
0. 退出系统
-----------------------------
"""
# 初始化操作标识，用户信息，操作面板
option, user_info, menu = -1, {}, main_menu
while option:
    if int(option) >= 0:
        option = int(option)
    else:
        print(menu)
        option = input("请输入操作序号>>:").strip()
        if option.isdigit():
            option = int(option)
        else:
            print(ERROR_USER_INPUT)
            option = -1
            continue
    # 用户退出系统
    if option == 0:
        if 'cart' in user_info:
            _cart_amount = 0
            if len(user_info['cart']):
                print("您的购物车清单如下：".center(50, '*'))
                print("序号".ljust(4), "商品".center(8, ' '), "金额".center(8, ' '), "数量".ljust(4))
                for i, log in enumerate(user_info['cart'][::-1], 1):
                    _cart_amount += log[1]
                    print("%s %s %s %s " % (
                        str(i).ljust(4), str(log[0]).center(8, ' '), str(float('%.2f' % log[1])).center(12, ' '),
                        str(log[2]).ljust(4)))
            else:
                print(ERROR_NO_RESULT)
            print("购物车总额:\033[92m%.2f\033[0m,您的账户余额:\033[92m%.2f\033[0m" % (_cart_amount, user_info['balance']))
        user_info = {}
        print(SUCCESS_USER_HALT)
        break
    # 用户登录
    elif option == 1:
        username = input("请输入登录账户，（9，返回）>>:").strip()
        if username == '9':
            menu = main_menu
            option = -1
            continue
        password = input("请输入登录密码>>:").strip()
        if len(username) <= 0 or len(password) <= 0:
            print(ERROR_USER_INPUT)
            menu = main_menu
            option = -1
            continue
        # 验证用户是否存在
        username_encypt = hashlib.md5()
        username_encypt.update(bytes(username, encoding='utf-8'))
        user_file = os.path.join(users_dir, ''.join([username_encypt.hexdigest(), '.json']))
        if not os.path.exists(user_file):
            print(ERROR_USER_NOT_EXISTS)
            option = 1
            continue
        # 验证登录密码，登录成功则进入用户中心
        user_info = json.load(open(user_file, 'r'))
        password_encypt = hashlib.md5()
        password_encypt.update(bytes(password, encoding='utf-8'))
        if 'password' in user_info and user_info['password'] == password_encypt.hexdigest():
            print("欢迎回来 \033[95m%s\033[0m ，您将进入用户中心面板" % username)
            menu = user_menu
            option = -1
        else:
            print(ERROR_USER_PASSWORD)
            option = 1
    # 用户注册
    elif option == 2:
        username = input("请输入用户账号，（9，返回）>>:").strip()
        if username == '9':
            menu = main_menu
            option = -1
            continue
        password = input("请输入用户密码>>:").strip()
        balance = input("请输入账户金额>>:").strip()
        # 检查输入是否合法
        if len(username) <= 0 or len(password) <= 0 or not balance.isdigit():
            print(ERROR_USER_INPUT)
            option = 2
            continue
        username_encypt = hashlib.md5()
        username_encypt.update(bytes(username, encoding='utf-8'))
        user_file = ''.join([username_encypt.hexdigest(), '.json'])
        # 检查是否已存在相同用户名
        user_exists = False
        for i in os.listdir(users_dir):
            if user_file == os.path.basename(i):
                user_exists = True
                break
        # 不存在则创建用户,创建成功直接进入用户中心
        if not user_exists:
            password_encypt = hashlib.md5()
            password_encypt.update(bytes(password, encoding='utf-8'))
            user_info = {
                'username': username,
                'password': password_encypt.hexdigest(),
                'balance': float(balance),
                'cart': [],
                'logs': [],
            }
            with open(os.path.join(users_dir, user_file), 'w') as f:
                json.dump(user_info, f)
            print(SUCCESS_USER_ADDED)
            menu = user_menu
            option = -1
        else:
            print(ERROR_USER_EXISTS)
            option = 2
    # 用户已登录
    elif option > 10:
        # 验证用户信息是否完整
        if 'username' not in user_info:
            print(ERROR_USER_LOGIN)
            menu = main_menu
            option = -1
            user_info = {}
            continue
        # 验证用户信息是否存档
        username_encypt = hashlib.md5()
        username_encypt.update(bytes(user_info['username'], encoding='utf-8'))
        user_file = os.path.join(users_dir, ''.join([username_encypt.hexdigest(), '.json']))
        if not os.path.exists(user_file):
            menu = main_menu
            option = -1
            user_info = {}
            continue
        # 购买商品
        if option == 11:
            menu = goods_menu
            option = -1
        # 查看购物车
        elif option == 12:
            _cart_amount = 0
            if len(user_info['cart']):
                print("您的购物车清单如下：".center(50, '*'))
                print("序号".ljust(4), "商品".center(8, ' '), "金额".ljust(12, ' '), "数量".ljust(4))
                for i, log in enumerate(user_info['cart'][::-1], 1):
                    _cart_amount += log[1]
                    print("%s %s %s %s " % (
                        str(i).ljust(4), str(log[0]).center(8, ' '), str(float('%.2f' % log[1])).center(12, ' '),
                        str(log[2]).ljust(4)))
            else:
                print(ERROR_EMPTY_CART)
            print("购物车总额:\033[92m%.2f\033[0m,您的账户余额:\033[92m%.2f\033[0m" % (_cart_amount, user_info['balance']))
            menu = user_menu
            option = -1
        # 查看账户流水
        elif option == 13:
            if len(user_info['logs']):
                print("序号".ljust(4), "时间".center(20, ' '), "商品".center(8, ' '), "金额".center(12, ' '), "备注".ljust(16))
                for i, log in enumerate(user_info['logs'][::-1], 1):
                    print("%s %s %s %s %s" % (
                        str(i).ljust(4), str(log[0]).center(20), str(log[1]).center(8),
                        str(float('%.2f' % log[2])).center(12),
                        str(log[3]).ljust(16)))
            else:
                print(ERROR_NO_RESULT)
            menu = user_menu
            option = -1
        # 帐户充值
        elif option == 14:
            balance = input("请输入充值金额，（b，返回；0，退出系统）>>:").strip()
            # 验证输入
            if balance == 'b':
                menu = user_menu
                option = -1
                continue
            elif balance == '0':
                option = 0
                continue
            elif not balance.isdigit():
                print(ERROR_USER_INPUT)
                option = 14
                continue
            # 更新用户信息，并存档
            user_info['balance'] += float(balance)
            user_info['logs'].append([time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), '账户充值', float(balance), ''])
            with open(user_file, 'w') as f:
                json.dump(user_info, f)
            print(SUCCESS_USER_RECHARGE, ', 您的余额：\033[92m%.2f\033[0m' % user_info['balance'])
            menu = user_menu
            option = -1
        # 修改密码
        elif option == 15:
            password = input("请输入新密码，（b，返回；0，退出系统）>>:").strip()
            # 验证输入
            if password == 'b':
                menu = user_menu
                option = -1
                continue
            elif password == '0':
                option = 0
                continue
            # 更新用户信息，并存档
            password_encypt = hashlib.md5()
            password_encypt.update(bytes(password, encoding='utf-8'))
            user_info['password'] = password_encypt.hexdigest()
            with open(user_file, 'w') as f:
                json.dump(user_info, f)
            print(SUCCESS_USER_REPASSWD)
            menu = user_menu
            option = -1
        # 选购商品
        elif option >= 100:
            if option == 999:
                menu = user_menu
                option = -1
                continue
            # 验证商品是否存在
            index = option - 100
            goods_exists = False
            for i, good in enumerate(goods):
                if i == index:
                    goods_exists = True
                    break
            if not goods_exists:
                print(ERROR_NO_GOODS)
                menu = goods_menu
                option = -1
                continue
            # 验证余额
            amount = float(goods[index]['price'])
            if user_info['balance'] < amount:
                print(ERROR_USER_BALANCE)
                menu = goods_menu
                option = -1
                continue
            # 更新用户余额信息，添加商品到购物车，添加记录到账户流水，重新存档用户信息
            user_info['balance'] -= amount
            user_info['cart'].append([goods[index]['name'], amount, 1])
            user_info['logs'].append(
                [time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), goods[index]['name'], amount, '数量：1'])
            with open(user_file, 'w') as f:
                json.dump(user_info, f)
            print(SUCCESS_USER_PURCHASED, ', 您的余额：\033[92m%.2f\033[0m' % user_info['balance'])
            menu = goods_menu
            option = -1
    else:
        print(ERROR_USER_INPUT)
        option = -1
