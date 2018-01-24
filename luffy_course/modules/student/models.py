#!/usr/bin/env python
# -*- coding:utf-8 -*-
# _AUTHOR_  : zhujingxiu
# _DATE_    : 2018/1/22

from core import utils
from libs.luffy_teacher import LuffyTeacher
from libs.luffy_course import LuffyCourse
from libs.luffy_class import LuffyClass
from libs.luffy_student import LuffyStudent


class Models:
    @staticmethod
    def profile(user):
        """
        显示个人信息
        :return: 
        """
        info = LuffyStudent.fetch_one(user.sn)
        print(info)

    @staticmethod
    @utils.log_or_catch
    def recharge(user, **kwargs):
        """
        创建班级
        :param user: 
        :param kwargs: 
        :return: 
        """
        amount = input("请输入充值金额，（b,返回）：>>").strip()
        if amount.lower() == 'b':
            return False
        if not amount.isdigit() and not utils.is_float_num(amount):
            print("请输入数字字符")
            return False

        entry = LuffyStudent.fetch_one(user.sn)
        entry.add_balance(float(amount))
        entry.add_transaction('%s 充值：%s' % (utils.calculate_date(time_format=True), amount))
        entry.save()
        return {'status': 0, 'logger': kwargs.get('logger'), 'msg': "学生 %s 成功充值 %s " % (entry.username, amount)}

    @staticmethod
    def show_classes(user, **kwargs):
        """
        显示班级列表
        :return: 
        """
        records = LuffyClass.fetch_all()
        print("班级列表")
        if not len(records):
            print("没有找到班级")
            return False
        classes = []
        for entry in records:
            if entry.school_sn == user.school_sn:
                classes.append(entry)
        if not len(classes):
            print("没有找到班级")
            return False
        for i, entry in enumerate(classes, 1):
            print('# ', i, entry)
        option = input("请输入要报名的班级ID（b，返回）:>>").strip()
        if option.lower() == 'b':
            return False
        index = int(option) - 1
        if index < 0 or index >= len(classes):
            print("错误的选项")
            return False

        Models.sign_up(user, **{'class': classes[index], 'logger': kwargs.get('logger')})

    @staticmethod
    @utils.log_or_catch
    def sign_up(user, **kwargs):
        selected = kwargs.get('class', False)
        if not selected:
            print("班级参数异常")
            return False
        student = LuffyStudent.fetch_one(user.sn)
        course = LuffyCourse.fetch_one(selected.course_sn)

        if float(student.get_balance()) < float(course.price):
            print('余额不足')
            return False
        # 更新学生余额及消费记录信息
        student.add_balance(-1 * float(course.price))
        student.add_transaction(
            '%s 报名课程：%s 价格：%s' % (utils.calculate_date(time_format=True), course.title, str(course.price)))
        student.save()
        # 更新班级学生列表
        selected.add_student(student.sn)
        selected.save()
        # 更新班级讲师的学生列表
        teacher = LuffyTeacher.fetch_one(selected.teacher_sn)
        teacher.add_student(student.sn)
        teacher.save()
        return {'status': 0, 'logger': kwargs.get('logger'),
                'msg': "报名课程：%s 价格：%s" % (course.title, str(course.price))}

    @staticmethod
    def show_transactions(user, **kwargs):
        student = LuffyStudent.fetch_one(user.sn)
        transactions = student.transactions()
        if not len(transactions):
            print("没有交易记录")
            return False
        for i, row in enumerate(transactions, 1):
            print('# ', i, row)

    @staticmethod
    def show_scores(user, **kwargs):
        student = LuffyStudent.fetch_one(user.sn)
        print(student.score())
