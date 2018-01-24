#!/usr/bin/env python
# -*- coding:utf-8 -*-
# _AUTHOR_  : zhujingxiu
# _DATE_    : 2018/1/24

import abc


class Service(metaclass=abc.ABCMeta):
    """
    定义服务接口
    """

    @classmethod
    @abc.abstractmethod
    def run(cls):
        pass

    @classmethod
    @abc.abstractmethod
    def interactive(cls, user=None):
        pass
