#!/usr/bin/env python
# -*- coding:utf-8 -*-
# _AUTHOR_  : zhujingxiu
# _DATE_    : 2018/1/9

#
# import random
#
# a = [1, 2, 3, 4, 5, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0]
# print("orginal:", a)
# print(list(set(a)))
#
# # str
# a = [float(i) for i in a]
# print("orginal:", a)
# print(list(set(a)))

# 通过句柄对文件进行操作
import subprocess
pretty = 'prettytable'
import pip
installed_packages = pip.get_installed_distributions()
pretty_installed = False
for i in installed_packages:
    if i.key == pretty:
        pretty_installed = True
        break

if not pretty_installed:
    subprocess.Popen('pip install %s' % pretty)

from prettytable import PrettyTable

table = PrettyTable(["animal", "ferocity"])
table.add_row(["wolverine", 100])
table.add_row(["grizzly", 87])
table.add_row(["Rabbit of Caerbannog", 110])
table.add_row(["cat", -1])
table.add_row(["platypus", 23])
table.add_row(["dolphin", 63])
table.add_row(["albatross", 44])
table.sort_key("ferocity")
table.reversesort = True
print(table)

#print(installed_packages.index(pretty))
#     print(i.key,i.version)
# installed_packages_list = sorted(["%s:%s" % (i.key, i.version) for i in installed_packages])
# print(installed_packages_list)