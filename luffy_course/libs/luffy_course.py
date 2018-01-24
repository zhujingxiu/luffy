#!/usr/bin/env python
# -*- coding:utf-8 -*-
# _AUTHOR_  : zhujingxiu
# _DATE_    : 2018/1/22
from core import utils
from conf import settings
from core.base_model import BaseModel
from libs.luffy_school import LuffySchool


class LuffyCourse(BaseModel):
    path = settings.DATABASE['tables'][settings.COURSE_TABLE]['file_path']

    def __init__(self, title, period, price, school_sn):
        self.sn = utils.sn()
        self.title = title
        self.period = period
        self.price = price
        self.school_sn = school_sn

    def __str__(self):
        """
        toString
        :return: 
        """
        return "课程：%s 周期：%s个月 价格：%s 学校：%s" % (
            self.title, self.period, self.price, LuffySchool.fetch_one(self.school_sn).title)
