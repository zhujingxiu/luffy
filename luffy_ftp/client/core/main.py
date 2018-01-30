#!/usr/bin/env python
# -*- coding:utf-8 -*-
# _AUTHOR_  : zhujingxiu
# _DATE_    : 2018/1/29
import os
from core.ftp_service import FTPService
from conf import settings


class Main:
    def __init__(self, addr):
        self.username = None
        self.hostname = None
        self.abs_path = None
        self.rel_path = None
        self.address = None
        self.service = FTPService(addr)

    def run(self):
        attempts = 0
        while attempts < settings.LOGIN_ATTEMPTS:
            username = input('请输入用户名（q，退出）:').strip()
            if username.lower() == 'q':
                self.service.close()
                exit("已退出系统")
            password = input('请输入密码:').strip()
            res = self.service.request(**{'action': 'auth', 'params': {'username': username, 'password': password}})

            if res.get('errorno') == 0:
                data = res.get('data')
                self.hostname = data.get('hostname')
                print("Welcome to %s " % self.hostname)
                self.abs_path = data.get('abspath')
                self.rel_path = data.get('relpath')
                self.username = username
                self.__interactive()
            else:
                print('账号或密码错误，请重新输入')
                attempts += 1
        else:
            exit("错误次数太多，已登出系统")

    def __interactive(self):
        while True:
            msg = input('[%s@%s %s]$ >> ' % (self.username, self.hostname, self.rel_path)).strip()
            msg_info = msg.split()
            action = "_%s__%s" % (self.__class__.__name__, msg_info[0])
            if hasattr(self, action):
                getattr(self, action)(*msg_info[1:])
            else:
                print('命令错误...')
                self.__help()

    def __pwd(self, *args):
        res = self.service.request(**{'action': 'pwd', 'params': {'path': self.abs_path}})
        if res.get('errorno') == 0:
            print(res.get('data'))
            return True
        else:
            print(res.get("errormsg"))
            return False

    def __help(self):
        print('''
            help 帮助信息
            put filename 上传文件
            get filename 下载文件
            pwd 当前路径
            cd path 切换目录
            ls path 查看目录
        ''')

    def __ls(self, *args):
        """
        查看目录 ls [path]
        :param args: 
        :return: 
        """
        if not len(args):
            path = self.abs_path
        else:
            path = args[0]
        res = self.service.request(**{'action': 'ls', 'params': {'path': path}})
        if res.get('errorno') == 0:
            print(res.get('data'))
            return True
        else:
            print(res.get("errormsg"))
            return False

    def __mkdir(self, *args):
        """
        创建文件夹 mkdir dir
        :param args: 
        :return: 
        """
        if not len(args):
            print("参数异常")
            return False
        if not str(args[0]).startswith("/") or not str(args[0]).startswith(os.sep):
            path = os.path.join(self.abs_path, args[0])
        else:
            path = args[0]
        res = self.service.request(**{'action': 'mkdir', 'params': {'path': path}})
        if res.get('errorno') == 0:
            print(res.get('data'))
            return True
        else:
            print(res.get("errormsg"))
            return False

    def __cd(self, *args):
        """
        目录切换 cd path
        :param args: 
        :return: 
        """
        if not len(args):
            path = self.rel_path
        else:
            path = args[0]
        res = self.service.request(**{'action': 'cd', 'params': {'path': path}})
        if res.get('errorno') == 0:
            data = res.get('data')
            self.abs_path = data.get('abspath')
            self.rel_path = data.get('relpath')
            return True
        else:
            print(res.get("errormsg"))
            return False

    def __put(self, *args):
        """
        上传文件 put filename 和客户端的启动文件在同级
        :param args: 
        :return: 
        """
        if not len(args):
            print("参数异常")
            return False
        filepath = args[0]
        if not os.path.isfile(filepath):
            print("文件异常")
            return False
        filesize = os.path.getsize(filepath)
        filename = os.path.basename(filepath)
        res = self.service.request(**{'action': 'put', 'params': {'filename': filename, 'filesize': filesize}})
        if res.get('errorno') == 0:
            print('开始上传文件[%s]大小[%s]' % (filename, Main.human_readable(filesize)))
            data = res.get('data')
            has_sent = data.get('has_sent', 0)
            if has_sent:
                inp_continue = input('文件已存在，是否续传Y/N？').strip()
                if inp_continue.lower() == "n":
                    has_sent = 0
            # 传送文件
            ret = self.service.send_file(filepath, has_sent)
            if ret.get('errorno') == 0:
                print("上传成功")
                return True
            else:
                print(res.get("errormsg"))
                return False
        else:
            print(res.get("errormsg"))
            return False

    def __get(self, *args):
        """
        获取文件 get filename
        :param args: 
        :return: 
        """
        if not len(args):
            print("参数异常")
            return False
        filepath = args[0]
        res = self.service.request(**{'action': 'get', 'params': {'filename': filepath}})
        if res.get('errorno') == 0:
            data = res.get('data')
            print('开始接收文件[%s]大小[%s]' % (data.get('filename'), Main.human_readable(data.get('filesize'))))
            has_recv = 0
            new_filepath = os.path.join(os.path.abspath(settings.DOWNLOAD_DIR), os.path.basename(filepath))
            if os.path.exists(new_filepath):
                has_recv = os.path.getsize(new_filepath)
                if has_recv == data.get('filesize'):
                    inp_continue = input('文件已存在，重命名文件或覆盖现有文件R/C？').strip()
                    has_recv = 0
                    if inp_continue.lower() == "r":
                        new_filepath = Main.rename_file(new_filepath)
                else:
                    inp_continue = input('文件已存在，是否续传Y/N？').strip()
                    if inp_continue.lower() == "n":
                        has_recv = 0
            # 接收文件
            ret = self.service.receive_file(new_filepath, filepath, data.get('filesize'), has_recv)

            if ret.get('errorno') == 0:
                if FTPService.file_md5(new_filepath) != data.get('filemd5'):
                    print("文件MD5校验失败")
                    return False
                print("文件下载成功")
                return True
            else:
                print(ret.get("errormsg"))
                return False

    @staticmethod
    def rename_file(filepath):
        """
        重命名文件
        :param filepath: 
        :return: 
        """
        import time
        return os.path.join(os.path.dirname(filepath),
                            ("." + str(int(time.time()))).join(os.path.splitext(os.path.basename(filepath))))

    @staticmethod
    def human_readable(plain_size):
        """
        格式化文件大小
        :param plain_size: 
        :return: 
        """
        plain_size = float(plain_size)
        if plain_size <= 1024:
            return str(round(plain_size, 2)) + 'B'
        if plain_size <= 1024 * 1024:
            return str(round(plain_size / 1024, 2)) + 'K'
        if plain_size <= 1024 * 1024 * 1024:
            return str(round(plain_size / 1024 / 1024, 2)) + 'M'
        if plain_size <= 1024 * 1024 * 1024 * 1024:
            return str(round(plain_size / 1024 / 1024 / 1024, 2)) + 'G'
