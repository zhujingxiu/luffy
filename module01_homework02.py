#!/usr/bin/env python
# -*- coding:utf-8 -*-
# _AUTHOR_  : zhujingxiu
# _DATE_    : 2018/1/4
import os
"""
作业题目: 三级菜单
需求：
可依次选择进入各子菜单
可从任意一层往回退到上一层
可从任意一层退出程序
所需新知识点：列表、字典
"""
menu = {
    '北京': {
        '海淀': {
            '五道口': {
                'soho': {},
                '网易': {},
                'google': {}
            },
            '中关村': {
                '爱奇艺': {},
                '汽车之家': {},
                'youku': {},
            },
            '上地': {
                '百度': {},
            },
        },
        '昌平': {
            '沙河': {
                '老男孩': {},
                '北航': {},
            },
            '天通苑': {},
            '回龙观': {},
        },
        '朝阳': {},
        '东城': {},
    },
    '上海': {
        '闵行': {
            "人民广场": {
                '炸鸡店': {}
            }
        },
        '闸北': {
            '火车战': {
                '携程': {}
            }
        },
        '浦东': {},
    },
    '山东': {},
}
"""
解题思路：
1.初次进入，父级节点为空，menu即作为当前层
2.进入子层后，将当前层追加入父节点，在当前层的目标节点作为当前层
3.返回上级：若父节点为空则说明是最顶层，否则，由于当前层已位于父节点的末尾，只要弹出父节点的末尾层作为当前层即可
"""
current, parent = menu, []
while True:
    destination = input(('%s请输入您的目的地' % (os.linesep.join(current.keys()) + os.linesep) if len(
        current) else '当前已无下级目的地') + ',(b|B,返回,q|Q,退出)>>:').strip()
    if destination.lower() == 'q':
        print('您已退出程序')
        break
    elif destination.lower() == 'b' and parent:
        current = parent.pop()
    elif destination in current:
        current, _ignore = current[destination], parent.append(current)
    else:
        print('不存在的下级')
