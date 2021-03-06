#!/usr/bin/env python
# -*- coding:utf-8 -*-
# _AUTHOR_  : zhujingxiu
# _DATE_    : 2018/1/22

from core import utils
from conf import settings
from core.base_model import BaseModel
from libs.luffy_school import LuffySchool


class LuffyStudent(BaseModel):
    path = settings.DATABASE['tables'][settings.STUDENT_TABLE]['file_path']

    def __init__(self, username, password, school_sn):
        self.sn = utils.sn()
        self.username = username
        self.password = password
        self.school_sn = school_sn
        self.__balance = 0
        self.__transaction = []
        self.__score = 0

    def add_balance(self, amount):
        """
        充值或消费
        :param amount: 
        :return: 
        """
        self.__balance += amount

    def get_balance(self):
        """
        获取余额
        :return: 
        """
        return self.__balance

    def add_transaction(self, transaction):
        """
        添加交易记录
        :param transaction: 
        :return: 
        """
        self.__transaction.append(transaction)

    def transactions(self):
        """
        获取交易记录
        :return: 
        """
        return self.__transaction

    def set_score(self, score):
        """
        打分
        :param score: 
        :return: 
        """
        self.__score = score

    def score(self):
        """
        获取成绩
        :return: 
        """
        return self.__score

    def __str__(self):
        return "学生：%s 余额：%s 得分：%s 学校：%s" % (
            self.username, self.__balance, self.__score, LuffySchool.fetch_one(self.school_sn).title)
