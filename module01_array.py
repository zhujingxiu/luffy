#!/usr/bin/env python
# -*- coding:utf-8 -*-
# _AUTHOR_  : zhujingxiu
# _DATE_    : 2018/1/8

#
# 创建列表
classmates = ['James', 'Michael', 'Bob', 'Tracy', 'Jason']
# 或者
my_classmates = list(['JackJons', 'Scofiled', 'Selected', 'H&M'])
print(classmates)  # ['James', 'Michael', 'Bob', 'Tracy', 'Jason']
# 索引通过下标访问列表中的元素，下标从0开始计数
print(classmates[0])  # James
print(classmates[-1])  # Jason
print(classmates.index('Michael'))  # 1
# 切片
print(classmates[0:2])  # ['James', 'Michael']
print(classmates[-3:4])  # ['Bob', 'Tracy']
# 增加
classmates.append('Andy')
classmates.insert(2, 'Jeff')
classmates.insert(-1, 'Linux')  # ['James', 'Michael', 'Jeff', 'Bob', 'Tracy', 'Jason', 'Linux', 'Andy']
print(classmates)

# 修改
classmates[1] = 'Mike'
# 删除
del classmates[4]
# print(classmates.remove("Eric")) #ValueError x not in list
classmates.append("Eric")
classmates.remove("Eric")
classmates.pop()
# 扩展
classmates.extend(['Peter', 'Jess', 'Tom', 'Bob'])
# 统计
print(classmates.count("Bob"))  # 2
# 排序
classmates.sort()
print(classmates)  # ['Bob', 'Bob', 'James', 'Jason', 'Jeff', 'Jess', 'Linux', 'Mike', 'Peter', 'Tom']
# 拷贝 （深浅拷贝）
classmates_new = classmates.copy()
print(classmates_new)  # ['Bob', 'Bob', 'James', 'Jason', 'Jeff', 'Jess', 'Linux', 'Mike', 'Peter', 'Tom']

ages = (11, 22, 33, 44, 55, 'python', True)
# 或
ages = tuple((11, 22, 33, 44, 55, 'python', True))
print(type(ages))  # <class 'tuple'>

# 字典
score = {'Michael': 95, 'Bob': 75, 'Tracy': 85}
print(score)
# 长度
print(len(score))
# 增加
score['Peter'] = 99
score['Gui'] = 'Python'
# 修改
score['Bob'] = 91
# 删除
del score['Tracy']
print(score.pop('Linux', '1989'))  # 1989 pop(key,default)删除并返回
# 是否存在
print('Bob' in score)
# 获取
print(score['Gui'])
print(score.get('Bob'))  # 91
print(score.get('Bobs', None))  # None
print(score.keys())  # dict_keys(['Michael', 'Bob', 'Peter', 'Gui'])
print(score.values())  # dict_values([95, 91, 99, 'Python'])
print(score.items())  # dict_items([('Michael', 95), ('Bob', 91), ('Peter', 99), ('Gui', 'Python')])
# 遍历
for stu in score:
    print(stu, score[stu])

for i, v in score.items():
    print(i, v)

# 嵌套
score['class3'] = score
print(score.items())
print('-' * 50)
# 集合
s = set([3, 5, 9, 10])  # 创建一个数值集合

t = set("Hello")  # 创建一个唯一字符的集合

a = t | s  # t 和 s的并集

b = t & s  # t 和 s的交集

c = t - s  # 求差集（项在t中，但不在s中）

d = t ^ s  # 对称差集（项在t或s中，但不会同时出现在二者中）

# 基本操作：

t.add('x')  # 添加一项

s.update([10, 37, 42])  # 在s中添加多项

# 使用remove()
# 可以删除一项：

t.remove('H')

print(len(s))  # 6
# set的长度
x = 10
print(x in s)  # True
# 测试x是否是s的成员

print(x not in s)  # False
# 测试x是否不是s的成员

print(s.issubset(t))  # False
print(s <= t)  # False
# 测试是否s中的每一个元素都在t中

print(s.issuperset(t))  # False
print(s >= t)  # False
# 测试是否t中的每一个元素都在s中

print(s.union(t))  # False
print(s | t)  # False
# 返回一个新的set，包含s和t中的每一个元素
print('*' * 50)
print(s.intersection(t))  # set()
print(s & t)  # set()
# 返回一个新的set，包含s和t中的公共元素

print(s.difference(t))  # {3, 5, 37, 9, 10, 42}
print(s - t)  # {3, 5, 37, 9, 10, 42}
# 返回一个新的set包含s中有但是t中没有的元素

print(s.symmetric_difference(t))  # {3, 37, 5, 9, 10, 42, 'l', 'x', 'o', 'e'}
print(s ^ t)  # {3, 37, 5, 9, 10, 42, 'l', 'x', 'o', 'e'}
# 返回一个新的set包含s和t中不重复的元素

sc = s.copy()
# 返回set “s”的一个浅复制
print(sc)  # {3, 37, 5, 9, 10, 42}
