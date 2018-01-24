#!/usr/bin/env python
# -*- coding:utf-8 -*-
# _AUTHOR_  : zhujingxiu
# _DATE_    : 2018/1/22
from core import utils
from conf import settings
from core.base_model import BaseModel
from libs.luffy_school import LuffySchool


class LuffyTeacher(BaseModel):
    path = settings.DATABASE['tables'][settings.TEACHER_TABLE]['file_path']

    def __init__(self, username, password, school_sn):
        self.sn = utils.sn()
        self.username = username
        self.password = utils.hash_md5(password)
        self.school_sn = school_sn
        self.__students = []
        self.__classes = []
        self.__duties = []

    def add_duty(self, duty):
        """
        执勤记录
        :param duty: 
        :return: 
        """
        self.__duties.append(duty)

    def duties(self):
        """
        返回执勤列表
        :return: 
        """
        return self.__duties

    def add_class(self, class_sn):
        """
        添加班级
        :param class_sn: 
        :return: 
        """
        self.__classes.append(class_sn)

    def classes(self):
        """
        返回班级列表
        :return: 
        """
        return self.__classes

    def add_student(self, student_sn):
        """
        添加学生
        :param student_sn: 
        :return: 
        """
        self.__students.append(student_sn)

    def students(self):
        """
        返回学生列表
        :return: 
        """
        return self.__students

    def __str__(self):
        return "讲师：%s 学校：%s 班级数：%s 学员数：%d" % (
            self.username, LuffySchool.fetch_one(self.school_sn).title, len(self.__classes), len(self.__students))
