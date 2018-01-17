#!/usr/bin/env python
# -*- coding:utf-8 -*-
# _AUTHOR_  : zhujingxiu
# _DATE_    : 2018/1/16




import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from conf import settings
from core import db_handler
from core import utils
from admin import models

# db_handler.find_action('users',**{'where': [{'field': 'id', 'value': 'sss'}, {'field': 'id', 'logic': '!=', 'value': 'sssss'}]})
# db_handler.data_api('find','users',**{'where': [{'field': 'id', 'value': 'sss'}, {'field': 'id', 'logic': '!=', 'value': 'sssss'}]})
# db_handler.add_action('users',**{'fields':{'id':'zjx123','password':'123','credit':15000,'balance':'15000'}})
# models.check_exists('users','zjx')
#print(models.get_increment_id('users'))
price = '1231wqewq123.45'
print(price, type(price), price.isnumeric(),price.isdecimal(), price.isdigit())
print(utils.is_float_num(price))
# print(db_handler.check_field(settings.USER_TABLE,*('*',)))
# db_handler.update_action('users',**{'set':{'id':'zjx111'},'where': [{'field': 'id', 'value': 'zjx'}]})
if settings.DATABASE['engine'] == 'mysql':
    add_args = {'id': 'zjx', 'password': 15}
    update_args = {'set': {'id': 'zjx', 'password': 15},
                   'where': [{'field': 'id', 'value': 'sss'}, {'field': 'id', 'logic': '!=', 'value': 'sssss'}]}
    find_args = {'fields': ['*'],
                 'where': [{'field': 'id', 'value': 'sss'}, {'field': 'id', 'logic': '!=', 'value': 'sssss'}]}
    print(db_handler.data_api('add', 'users', **add_args))
    print(db_handler.data_api('update', 'users', **update_args))
    print(db_handler.data_api('find', 'users', **find_args))
