#!/usr/bin/env python
# -*- coding:utf-8 -*-
# _AUTHOR_  : zhujingxiu
# _DATE_    : 2018/1/22

from core import utils
from conf import settings
from core.base_model import BaseModel


class LuffySchool(BaseModel):
    path = settings.DATABASE['tables'][settings.SCHOOL_TABLE]['file_path']

    def __init__(self, title):
        self.sn = utils.sn()
        self.title = title
        self.__teachers = []
        self.__classes = []
        self.__courses = []
        self.__students = []

    def add_teacher(self, teacher_sn):
        """
        添加教师
        :param teacher_sn: 
        :return: 
        """
        self.__teachers.append(teacher_sn)

    def remove_teacher(self, teacher_sn):
        """
        移除教师
        :param teacher_sn: 
        :return: 
        """
        if teacher_sn in self.__teachers:
            self.__teachers.remove(teacher_sn)

    def teachers(self):
        """
        返回教师列表
        :return: 
        """
        return self.__teachers

    def add_course(self, course_sn):
        """
        添加课程
        :param course_sn: 
        :return: 
        """
        self.__courses.append(course_sn)

    def remove_course(self, course_sn):
        """
        移除课程
        :param course_sn: 
        :return: 
        """
        if course_sn in self.__courses:
            self.__courses.remove(course_sn)

    def courses(self):
        """
        返回课程列表
        :return: 
        """
        return self.__courses

    def add_class(self, class_sn):
        """
        添加班级
        :param class_sn: 
        :return: 
        """
        self.__classes.append(class_sn)

    def remove_class(self, class_sn):
        """
        移除班级
        :param class_sn: 
        :return: 
        """
        if class_sn in self.__classes:
            self.__classes.remove(class_sn)

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

    def remove_student(self, student_sn):
        """
        移除学生
        :param student_sn: 
        :return: 
        """
        if student_sn in self.__students:
            self.__students.remove(student_sn)

    def students(self):
        """
        返回学生列表
        :return: 
        """
        return self.__students

    def __str__(self):
        return "学校：%s 讲师数：%d 班级数：%d 课程数：%d 学生数：%d" % (
            self.title, len(self.__teachers), len(self.__classes), len(self.__courses), len(self.__students))
