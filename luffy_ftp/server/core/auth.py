#!/usr/bin/env python
# -*- coding:utf-8 -*-
# _AUTHOR_  : zhujingxiu
# _DATE_    : 2018/1/29
import os
import configparser
from . import utils
from conf import settings


class Auth:
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read(settings.ACCOUNT_FILE, encoding='utf-8')

    def authentication(self, username, password):
        if not self.config.has_section(username) or not self.config.has_option(username, 'password'):
            return False
        if self.config.get(username, 'password') == utils.hash_md5(password):
            return {
                'username':username,
                'quota':utils.format_filesize(self.config.get(username, 'quota')),
                'home_dir':self.__check_home(username)
            }
        return False

    def __check_home(self,username):
        user_home = os.path.join(settings.HOME_DIR, username)
        if not os.path.isdir(user_home):
            os.mkdir(user_home)

        return user_home

    def create_user(self,username,password,quota=1024):

        if not self.config.has_section(username):
            self.config.add_section(username)
            self.__check_home(username)
        self.config.set(username, 'password', utils.hash_md5(password))
        self.config.set(username, 'quota', "%sM" % quota)
        self.config.write(open(settings.ACCOUNT_FILE, 'w+', encoding='utf-8'))
        return True

