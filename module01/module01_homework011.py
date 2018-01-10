#!/usr/bin/env python
# -*- coding:utf-8 -*-
# _AUTHOR_  : zhujingxiu
# _DATE_    : 2018/1/3

# 作业题目: 编写登陆认证程序
'''
基础需求：
让用户输入用户名密码
认证成功后显示欢迎信息
输错三次后退出程序
'''
import hashlib

m = hashlib.md5()
m.update(bytes("Hello",encoding='utf-8'))
#m.update("It's me")

print(m.hexdigest())
#m.update("It's been a long time since last time we ...")
m = hashlib.md5()
m.update(bytes("Hello",encoding='utf-8'))
print(m.hexdigest())  # 2进制格式hash
#print(len(m.hexdigest()))  # 16进制格式hash
# counter = 0
# max_times = 3
# while counter < max_times :
#
#     username = input('请输入用户名>>')
#     password = input('请输入密码>>')
#
#     if username == 'python' and password == '1989' :
#         print('欢迎回来 %s !' % username)
#         break
#     else :
#         counter += 1
#
# else:
#     print('登录失败次数已达最大值，您已被强制退出')