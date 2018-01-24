#!/usr/bin/env python
# -*- coding:utf-8 -*-
# _AUTHOR_  : zhujingxiu
# _DATE_    : 2018/1/22
from core import utils
from conf import settings
from core.base_model import BaseModel
from libs.luffy_school import LuffySchool
from libs.luffy_course import LuffyCourse
from libs.luffy_teacher import LuffyTeacher


class LuffyClass(BaseModel):
    path = settings.DATABASE['tables'][settings.CLASS_TABLE]['file_path']

    def __init__(self, title, school_sn, course_sn, teacher_sn):
        self.sn = utils.sn()
        self.title = title
        self.school_sn = school_sn
        self.teacher_sn = teacher_sn
        self.course_sn = course_sn
        self.__students = []
        self.__duties = []

    def add_duty(self, duty):
        """
        执勤记录
        :param duty: 
        :return: 
        """
        self.__duties.append(duty)

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
        return "班级：%s 学校：%s 课程：%s 讲师：%s 学员数：%d" % (
            self.title, LuffySchool.fetch_one(self.school_sn).title, LuffyCourse.fetch_one(self.course_sn).title,
            LuffyTeacher.fetch_one(self.teacher_sn).username, len(self.__students))
