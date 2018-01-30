#!/usr/bin/env python
# -*- coding:utf-8 -*-
# _AUTHOR_  : zhujingxiu
# _DATE_    : 2018/1/29
from core.auth import Auth
from core.ftp_service import FTPService


class Main:
    @staticmethod
    def service():
        inp = input("创建FTP用户|启动FTPServer，A|其他任意键:>>")
        if inp.lower() == 'a':
            while True:
                username = input("输入用户名：>>").strip()
                password = input("输入密码：>>").strip()
                quota = input("设定家目录大小(Mb)：>>").strip()
                if not quota.isdigit():
                    print("请输入数字字符")
                    inp_continue = input("退出或重新录入，q|其他任意键：>>").strip()
                    if inp_continue.lower() == 'q':
                        break
                    continue
                if Auth().create_user(username, password, quota):
                    break
        else:
            FTPService().run()
