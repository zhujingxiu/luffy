#!/usr/bin/env python
# -*- coding:utf-8 -*-
# _AUTHOR_  : zhujingxiu
# _DATE_    : 2018/1/22

import os
import logging

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 后台默认的管理员账户
ADMIN_ACCOUNT = 'admin'
ADMIN_PASSWORD = 'admin'

# 可尝试登陆次数
LOGIN_ATTEMPTS = 3

# 日志存档目录
LOG_PATH = os.path.join(BASE_DIR, 'logs')
# 日志级别
LOG_LEVEL = logging.INFO
# 允许的日志类型
LOG_TYPES = {
    'teacher': 'teacher.log',
    'student': 'student.log',
    'admin': 'admin.log',
}
# 日志格式
LOG_FORMATTER = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

SCHOOL_TABLE = 'school'
TEACHER_TABLE = 'teacher'
CLASS_TABLE = 'class'
COURSE_TABLE = 'course'
STUDENT_TABLE = 'student'
DATABASE = {
    'engine': 'file_storage',  # file_storage,support mysql in the future
    'file_path': os.path.join(BASE_DIR, 'db'),
    'tables': {
        SCHOOL_TABLE: {
            'file_path': os.path.join(BASE_DIR, 'db', SCHOOL_TABLE)
        },
        TEACHER_TABLE: {
            'file_path': os.path.join(BASE_DIR, 'db', TEACHER_TABLE)
        },
        CLASS_TABLE: {
            'file_path': os.path.join(BASE_DIR, 'db', CLASS_TABLE)
        },
        COURSE_TABLE: {
            'file_path': os.path.join(BASE_DIR, 'db', COURSE_TABLE)
        },
        STUDENT_TABLE: {
            'file_path': os.path.join(BASE_DIR, 'db', STUDENT_TABLE)
        }
    }
}
