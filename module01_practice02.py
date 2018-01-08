#!/usr/bin/env python
# -*- coding:utf-8 -*-
# _AUTHOR_  : zhujingxiu
# _DATE_    : 2018/1/4

#
import time

print(time.strftime("%Y-%m-%d %H:%M:%S",time.localtime()))
'''
1. 下划线拼接列表元素
'''

goods = [
    {"name": "电脑", "price": 1999},
    {"name": "鼠标", "price": 10},
    {"name": "游艇", "price": 20},
    {"name": "美女", "price": 998},
    {"name": "机器人", "price": 2998},
    {"name": "特斯拉", "price": 5998}
]

for i,good in enumerate(goods):
    print(i)
# li = ['alex', 'eric', 'rain']
#
# print('_'.join(li))
#
# li = ["alec", " aric", "Alex", "Tony", "rain"]
# tu = ("alec", " aric", "Alex", "Tony", "rain")
# dic = {'k1': "alex", 'k2': ' aric', "k3": "Alex", "k4": "Tony"}
# new_li = []
# for i,v in li:
#     print(i)
#     new_li.insert(i,v.strip())
#
# print(new_li)
