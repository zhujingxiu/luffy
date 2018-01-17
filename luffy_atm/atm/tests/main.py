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
from atm12 import models
import time
print(time.time())
# print(models.load_user('zhujingxiu'))
fields = ('id', 'title', 'price', 'number', 'status')
ret = db_handler.data_api('find', settings.PRODUCT_TABLE, **{'fields': fields})

user = {"id": 3, "username": "luffy", "password": "123", "credit": 12345.0, "balance": 12345.0, "enroll_date": "2018-01-16", "expire_date": "2023-01-16", "status": 0, "cart": {}}

