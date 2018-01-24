#!/usr/bin/env python
# -*- coding:utf-8 -*-
# _AUTHOR_  : zhujingxiu
# _DATE_    : 2018/1/22

from core import utils
from libs.luffy_teacher import LuffyTeacher
from libs.luffy_student import LuffyStudent
from libs.luffy_class import LuffyClass


class Models:
    @staticmethod
    def profile(user):
        """
        显示个人信息
        :return: 
        """
        info = LuffyTeacher.fetch_one(user.sn)
        print(info)

    @staticmethod
    def show_classes(user, **kwargs):
        """
        显示讲师的班级列表
        :param user: 
        :param kwargs: 
        :return: 
        """
        teacher = LuffyTeacher.fetch_one(user.sn)
        classes = teacher.classes()
        if not len(classes):
            print("没有班级记录")
            return False
        records = []
        for sn in classes:
            entry = LuffyClass.fetch_one(sn)
            if entry:
                records.append(entry)
        if not len(records):
            print("没有班级记录")
            return False
        for i, row in enumerate(records, 1):
            print('# ', i, row)
        option = input("请输入要上课的班级ID（b，返回）:>>").strip()
        if option.lower() == 'b':
            return False
        index = int(option) - 1
        if index < 0 or index >= len(records):
            print("错误的选项")
            return False
        Models.add_duty(user, **{'class': records[index], 'logger': kwargs.get('logger')})

    @staticmethod
    @utils.log_or_catch
    def add_duty(user, **kwargs):
        """
        给学生打分
        :param user: 
        :param kwargs: 
        :return: 
        """
        selected = kwargs.get('class', False)
        if not selected:
            print("班级参数异常")
            return False
        selected.add_duty(
            "%s 讲师 %s 在班级 %s 上课" % (utils.calculate_date(time_format=True), user.username, selected.title))
        selected.save()
        user.add_duty("%s 在班级 %s 上课" % (utils.calculate_date(time_format=True), selected.title))
        user.save()
        return {'status': 0, 'logger': kwargs.get('logger'),
                'msg': "讲师 %s 添加上课记录：在班级%s上课" % (user.username, selected.title)}

    @staticmethod
    def show_students(user, **kwargs):
        """
        显示讲师的学生列表
        :param user: 
        :param kwargs: 
        :return: 
        """
        teacher = LuffyTeacher.fetch_one(user.sn)
        students = teacher.students()
        if not len(students):
            print("没有学生记录")
            return False
        records = []
        for sn in students:
            entry = LuffyStudent.fetch_one(sn)
            if entry:
                records.append(entry)
        if not len(records):
            print("没有学生记录")
            return False
        for i, row in enumerate(records, 1):
            print('# ', i, row)
        option = input("请输入要打分的学生ID（b，返回）:>>").strip()
        if option.lower() == 'b':
            return False
        index = int(option) - 1
        if index < 0 or index >= len(records):
            print("错误的选项")
            return False
        score = input("请输入分值:>>").strip()
        if not score.isdigit() and not utils.is_float_num(score):
            print("请输入数字字符")
            return False
        Models.set_score(user, **{'student': records[index], 'score': score, 'logger': kwargs.get('logger')})

    @staticmethod
    @utils.log_or_catch
    def set_score(user, **kwargs):
        """
        给学生打分
        :param user: 
        :param kwargs: 
        :return: 
        """
        selected = kwargs.get('student', False)
        score = kwargs.get('score', 0)
        if not selected:
            print("学生参数异常")
            return False
        student = LuffyStudent.fetch_one(selected.sn)
        student.set_score(score)
        student.save()
        return {'status': 0, 'logger': kwargs.get('logger'),
                'msg': "讲师 %s 修改学员 %s 分值为：%s" % (user.username, student.username, str(score))}

    @staticmethod
    def show_duties(user,**kwargs):
        teacher = LuffyTeacher.fetch_one(user.sn)
        duties = teacher.duties()
        if not len(duties):
            print("没有执勤记录")
            return False

        for i,row in enumerate(duties,1):
            print('# ',i,row)

        return duties