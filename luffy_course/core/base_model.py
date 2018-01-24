#!/usr/bin/env python
# -*- coding:utf-8 -*-
# _AUTHOR_  : zhujingxiu
# _DATE_    : 2018/1/22
import os
import pickle


class BaseModel:

    @classmethod
    def fetch_all(cls):
        """
        获取全部记录
        :return: 
        """
        records = []
        for file in os.listdir(cls.path):
            file_path = os.path.join(cls.path, file)
            if os.path.isfile(file_path):
                entry = pickle.load(open(file_path, 'rb'))
                records.append(entry)
        return records

    @classmethod
    def fetch_one(cls, sn):
        """
        由sn获取单一记录
        :param sn: 
        :return: 
        """
        file_path = BaseModel.entry_file(cls.path, sn)
        if os.path.isfile(file_path):
            return pickle.load(open(file_path, 'rb'))
        return False

    @staticmethod
    def entry_file(path, sn):
        """
        获取记录文件路径
        :param path: 
        :param sn: 
        :return: 
        """
        return os.path.join(path, sn)

    def save(self):
        """
        持久化到文件
        :return: 
        """
        pickle.dump(self, open(BaseModel.entry_file(self.path, self.sn), 'wb'))
