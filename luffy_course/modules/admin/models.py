#!/usr/bin/env python
# -*- coding:utf-8 -*-
# _AUTHOR_  : zhujingxiu
# _DATE_    : 2018/1/22
from conf import settings
from core import utils
from libs.luffy_school import LuffySchool
from libs.luffy_teacher import LuffyTeacher
from libs.luffy_course import LuffyCourse
from libs.luffy_class import LuffyClass


class Models:
    @staticmethod
    def show_schools():
        """
        显示学校
        :return: 
        """
        records = LuffySchool.fetch_all()
        print("学校列表")
        if not len(records):
            print("没有找到学校")
            return []
        for i, entry in enumerate(records, 1):
            print('# ', i, entry)
        return records

    @staticmethod
    @utils.log_or_catch
    def create_school(**kwargs):
        """
        创建学校
        :param kwargs:title,学校名称;city,所在城市
        :return: 
        """
        title = input("请输入学校名称，（b,返回）：>>").strip()
        if title.lower() == 'b':
            return False
        if not len(title):
            print('名称不得为空')
            return False
        entry = LuffySchool(title)
        entry.save()
        return {'status': 0, 'logger': kwargs.get('logger'), 'msg': "学校 %s 创建成功" % title}

    @staticmethod
    @utils.log_or_catch
    def update_school(**kwargs):
        """
        修改学校工厂方法
        :param kwargs: name,学校名称;city,所在城市 
        :return: 
        """

        entries = Models.show_schools()
        if not len(entries):
            return False
        entry_id = input("请输入学校序号（b,返回）：>>").strip()
        if entry_id.lower() == 'b':
            return False
        index = int(entry_id) - 1
        if index < 0 or index >= len(entries):
            print("错误的选项")
            return False
        entry = entries[index]
        title = input("请重新输入学校名称（b,返回）：>>").strip()
        if title.lower() == 'b':
            return False
        if not len(title):
            print('名称不得为空')
            return False
        entry.title = title
        entry.save()
        return {'status': 0, 'logger': kwargs.get('logger'), 'msg': "学校 %s 修改成功" % title}

    @staticmethod
    def show_teachers(school_sn=False):
        """
        显示讲师列表
        :return: 
        """
        records = LuffyTeacher.fetch_all()
        print("讲师列表")
        if not len(records):
            print("没有找到讲师")
            return []
        result = []
        for entry in records:
            if school_sn and entry.school_sn != school_sn:
                continue
            result.append(entry)

        for i, entry in enumerate(result, 1):
            print('# ', i, entry)
        return result

    @staticmethod
    @utils.log_or_catch
    def create_teacher(**kwargs):
        """
        创建讲师工厂方法
        :param kwargs:name,讲师名称;age,讲师年纪;school_sn,学校序列号 
        :return: 
        """
        username = input("请输入讲师名称，（b,返回）：>>").strip()
        if username.lower() == 'b':
            return False
        if not len(username):
            print('讲师名称不得为空')
            return False
        password = input("请输入讲师登录密码，（b,返回）：>>").strip()

        schools = Models.show_schools()
        entry_id = input("请输入讲师的学校序号：>>").strip()
        index = int(entry_id) - 1
        if index < 0 or index >= len(schools):
            print("错误的选项")
            return False
        # 更新讲师信息和学校的讲师信息
        school = schools[index]
        entry = LuffyTeacher(username, password, school.sn)
        entry.save()
        school.add_teacher(entry.sn)
        school.save()
        return {'status': 0, 'logger': kwargs.get('logger'), 'msg': "讲师 %s 创建成功" % username}

    @staticmethod
    @utils.log_or_catch
    def update_teacher(**kwargs):
        """
        修改课程
        :param kwargs: name,讲师名称;age,讲师年纪;school_sn,学校序列号 
        :return: 
        """
        entries = Models.show_teachers()
        if not len(entries):
            return False
        entry_id = input("请输入讲师序号（b,返回）：>>").strip()
        if entry_id.lower() == 'b':
            return False
        index = int(entry_id) - 1

        if index < 0 or index >= len(entries):
            print("错误的选项")
            return False
        entry = entries[index]
        username = input("请重新输入讲师名称，（b,返回）：>>").strip()
        if username.lower() == 'b':
            return False
        if not len(username):
            print('讲师名称不得为空')
            return False

        password = input("请输入讲师登录密码：>>").strip()
        schools = Models.show_schools()
        entry_id = input("请重新输入讲师的学校序号：>>").strip()
        index = int(entry_id) - 1
        if index < 0 or index >= len(schools):
            print("错误的选项")
            return False

        # 删除原学校的该教师sn
        old_school = LuffySchool.fetch_one(entry.school_sn)
        old_school.remove_teacher(entry.sn)
        old_school.save()
        # 更新教师信息和学校的老师信息
        school = schools[index]
        entry.username = username
        entry.password = password
        entry.school_sn = school.sn
        entry.save()
        school.add_teacher(entry.sn)
        school.save()

        return {'status': 0, 'logger': kwargs.get('logger'), 'msg': "讲师 %s 修改成功" % username}

    @staticmethod
    def show_courses(school_sn=False):
        """
        显示课程列表
        :return: 
        """
        records = LuffyCourse.fetch_all()
        print("课程列表")
        if not len(records):
            print("没有找到课程")
            return []
        result = []
        for entry in records:
            if school_sn and entry.school_sn != school_sn:
                continue
            result.append(entry)

        for i, entry in enumerate(result, 1):
            print('# ', i, entry)
        return result

    @staticmethod
    @utils.log_or_catch
    def create_course(**kwargs):
        """
        创建课程
        :param kwargs: title,课程名称;period,课程周期;price,课程价格；school_sn,所在学校 
        :return: 
        """
        title = input("请输入课程名称，（b,返回）：>>").strip()
        if title.lower() == 'b':
            return False
        if not len(title):
            print('课程名称不得为空')
            return False
        period = input("请输入课程周期（月）：>>").strip()
        if not period.isdigit():
            print("请输入数字字符")
            return False
        price = input("请输入课程价格：>>").strip()
        if not price.isdigit() and not utils.is_float_num(price):
            print("请输入数字字符")
            return False
        schools = Models.show_schools()
        entry_id = input("请输入课程所属学校序号：>>").strip()
        index = int(entry_id) - 1
        if index < 0 or index >= len(schools):
            print("错误的选项")
            return False
        # 更新课程信息和学校的课程信息
        school = schools[index]
        entry = LuffyCourse(title, period, price,school.sn)
        entry.save()
        school.add_course(entry.sn)
        school.save()
        return {'status': 0, 'logger': kwargs.get('logger'), 'msg': "课程 %s 创建成功" % title}

    @staticmethod
    @utils.log_or_catch
    def update_course(**kwargs):
        """
        修改课程
        :param kwargs: title,课程名称;period,课程周期;price,课程价格；school_sn,所在学校
        :return: 
        """
        entries = Models.show_courses()
        if not len(entries):
            return False
        entry_id = input("请输入学校序号（b,返回）：>>").strip()
        if entry_id.lower() == 'b':
            return False
        index = int(entry_id) - 1
        if index < 0 or index >= len(entries):
            print("错误的选项")
            return False
        entry = entries[index]
        title = input("请重新输入课程名称，（b,返回）：>>").strip()
        if title.lower() == 'b':
            return False
        if not len(title):
            print('课程名称不得为空')
            return False
        period = input("请重新输入课程周期（月）：>>").strip()
        if not period.isdigit():
            print("请输入数字字符")
            return False
        price = input("请重新输入课程价格：>>").strip()
        if not price.isdigit() and not utils.is_float_num(price):
            print("请输入数字字符")
            return False
        schools = Models.show_schools()
        school_id = input("请重新输入课程所属学校序号：>>").strip()
        index = int(school_id) - 1
        if index < 0 or index >= len(schools):
            print("错误的选项")
            return False
        # 删除原学校的该课程sn
        old_school = LuffySchool.fetch_one(entry.school_sn)
        old_school.remove_course(entry.sn)
        old_school.save()
        # 更新课程新信息和学校的课程信息
        school = schools[index]
        entry.title = title
        entry.period = period
        entry.price = price
        entry.school_sn = school.sn
        entry.save()
        school.add_course(entry.sn)
        school.save()
        return {'status': 0, 'logger': kwargs.get('logger'), 'msg': "课程 %s 修改成功" % title}

    @staticmethod
    def show_classes():
        """
        显示班级列表
        :return: 
        """
        records = LuffyClass.fetch_all()
        print("班级列表")
        if not len(records):
            print("没有找到班级")
            return []
        for i, entry in enumerate(records, 1):
            print('# ', i, entry)
        return records

    @staticmethod
    @utils.log_or_catch
    def create_class(**kwargs):
        """
        创建班级
        :param kwargs: 
        :return: 
        """
        title = input("请输入班级名称，（b,返回）：>>").strip()
        if title.lower() == 'b':
            return False
        if not len(title):
            print('班级名称不得为空')
            return False
        schools = Models.show_schools()
        if not len(schools):
            return False
        school_id = input("请输入班级所属学校序号：>>").strip()
        school_index = int(school_id) - 1
        if school_index < 0 or school_index >= len(schools):
            print("错误的选项")
            return False
        school = schools[school_index]
        courses = Models.show_courses(school.sn)
        if not len(courses):
            return False
        course_id = input("请输入班级的课程序号（b,返回）：>>").strip()
        course_index = int(course_id) - 1
        if course_index < 0 or course_index >= len(courses):
            print("错误的选项")
            return False

        teachers = Models.show_teachers(school.sn)
        if not len(teachers):
            return False
        teacher_id = input("请输入班级的讲师序号：>>").strip()
        teacher_index = int(teacher_id) - 1
        if teacher_index < 0 or teacher_index >= len(teachers):
            print("错误的选项")
            return False
        teacher = teachers[teacher_index]

        # 添加班级信息并更新学校班级列表和讲师班级列表
        entry = LuffyClass(title, school.sn,courses[course_index].sn, teacher.sn)
        entry.save()
        school.add_class(entry.sn)
        school.save()
        teacher.add_class(entry.sn)
        teacher.save()
        return {'status': 0, 'logger': kwargs.get('logger'), 'msg': "班级 %s 创建成功" % title}

    @staticmethod
    @utils.log_or_catch
    def update_class(**kwargs):
        """
        创建学校工厂方法
        :param kwargs: name,学校名称;city,所在城市 
        :return: 
        """
        entries = Models.show_classes()
        if not len(entries):
            return False
        entry_id = input("请输入班级序号（b,返回）：>>").strip()
        if entry_id.lower() == 'b':
            return False
        index = int(entry_id) - 1
        if index < 0 or index >= len(entries):
            print("错误的选项")
            return False
        entry = entries[index]
        title = input("请重新输入班级名称，（b,返回）：>>").strip()
        if title.lower() == 'b':
            return False
        if not len(title):
            print('班级名称不得为空')
            return False
        schools = Models.show_schools()
        if not len(schools):
            return False
        school_id = input("请重新输入班级所属学校序号：>>").strip()
        school_index = int(school_id) - 1
        if school_index < 0 or school_index >= len(schools):
            print("错误的选项")
            return False
        school = schools[school_index]
        courses = Models.show_courses(school.sn)
        if not len(courses):
            return False
        course_id = input("请重新输入班级的课程序号：>>").strip()
        course_index = int(course_id) - 1
        if course_index < 0 or course_index >= len(courses):
            print("错误的选项")
            return False
        teachers = Models.show_teachers(school.sn)
        if not len(teachers):
            return False
        teacher_id = input("请重新输入班级的讲师序号：>>").strip()
        teacher_index = int(teacher_id) - 1
        if teacher_index < 0 or teacher_index >= len(teachers):
            print("错误的选项")
            return False
        teacher = teachers[teacher_index]
        # 删除学校班级列表中的该班级sn
        old_school = LuffySchool.fetch_one(entry.school_sn)
        old_school.remove_class(entry.sn)
        old_school.save()
        # 修改班级信息并更新学校班级列表和讲师班级列表
        entry.title = title
        entry.school_sn = school.sn
        entry.course_sn = courses[course_index].sn
        entry.teacher_sn = teacher.sn
        entry.save()
        school.add_class(entry.sn)
        school.save()
        teacher.add_class(entry.sn)
        teacher.save()
        return {'status': 0, 'logger': kwargs.get('logger'), 'msg': "班级 %s 修改成功" % title}
