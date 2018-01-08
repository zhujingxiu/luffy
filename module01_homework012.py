#!/usr/bin/env python
# -*- coding:utf-8 -*-
# _AUTHOR_  : zhujingxiu
# _DATE_    : 2018/1/3

"""
作业题目: 编写登陆认证程序
基础需求:
让用户输入用户名密码
认证成功后显示欢迎信息
输错三次后退出程序

升级需求:
可以支持多个用户登录 (提示，通过列表存多个账户信息)，为啥不说用字典存储呢
用户3次认证失败后，退出程序，再次启动程序尝试登录时，还是锁定状态（提示:需把用户锁定的状态存到文件里）
"""
#用户列表
users = [['python','django'],['php','web123'],['java','coffee'],['linux','ubuntu']]
#锁定用户文件
locked_file = 'module01_homework012_login_locked.txt'
# 最大登录失败次数
max_times = 3
# 登录失败用户列表
failed_users = []

while True:
    username = input('请输入用户名>>')
    password = input('请输入密码>>')

    # 读取已被锁定的用户文件
    locked_str = ''
    with open(locked_file, 'r+') as f:
        locked_str = f.read()   #数据比较小，就直接读了，文件比较大的需用缓存读取

    locked_users = locked_str.split('|')
    # 若已在被锁定名单内则直接退出
    if username in locked_users:
        print('登录失败次数已达最大值，您的账户已被锁定')
        break

    filter_times = 0
    # 遍历用户列表
    for user in users:
        _username , _password = user
        if username == _username:
            # 用户名密码匹配则登录成功
            if password == _password:
                print('欢迎回来 %s !' % username)
                if username in failed_users:
                    failed_users.remove(username)       #也可遍历删除所有同名
                break
            else:
                print('用户名和密码不匹配')
                # 若失败列表中的存储的用户名个数已达最大数，则保存到锁定文件中，否则将用户名再次添加到失败列表中
                failed_users.append(username)
                if failed_users.count(username) >= max_times:
                    print('登录失败次数已达最大值，您的账户已被锁定')
                    with open(locked_file,'a+') as f:
                        f.write(''.join([username,'|']))
                    break

                #print(failed_users) 调试
        else:
            filter_times += 1
    #遍历完用户表依然找不到存在的用户名，提示用户名不存在
    if filter_times == len(users):
        print('用户不存在')
