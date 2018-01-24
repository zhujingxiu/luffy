#!/usr/bin/env python
# -*- coding:utf-8 -*-
# _AUTHOR_  : zhujingxiu
# _DATE_    : 2018/1/22
import os
from conf import settings
from modules.admin.main import Main as AdminService
from modules.teacher.main import Main as TeacherService
from modules.student.main import Main as StudentService


class Controller:
    @staticmethod
    def initialize():
        """
        初始化系统参数
        :return: 
        """
        if not os.path.exists(settings.LOG_PATH):
            os.mkdir(settings.LOG_PATH)

        if settings.DATABASE['engine'] == 'file_storage':
            if not os.path.exists(settings.DATABASE['file_path']):
                os.mkdir(settings.DATABASE['file_path'])
            for table in settings.DATABASE['tables']:

                if not os.path.exists(settings.DATABASE['tables'][table]['file_path']):
                    os.mkdir(settings.DATABASE['tables'][table]['file_path'])

    @staticmethod
    def dispatch(instance):
        """
        分发到对应的服务接口
        :param instance: 
        :return: 
        """
        Controller.initialize()
        services = {
            'admin': AdminService,
            'teacher': TeacherService,
            'student': StudentService,
        }
        if instance not in services.keys():
            print('未知的服务接口')
            exit(0)
        services.get(instance).run()
