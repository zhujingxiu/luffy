#!/usr/bin/env python
# -*- coding:utf-8 -*-
# _AUTHOR_  : zhujingxiu
# _DATE_    : 2018/1/29
import os
import sys
import socket
import struct
import json
from conf import settings


class FTPService:
    def __init__(self, addr):
        try:
            if not os.path.exists(settings.DOWNLOAD_DIR):
                os.mkdir(settings.DOWNLOAD_DIR)
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect_ex(addr)
        except ConnectionRefusedError as e:
            exit("服务器错误：%s，请确认FTP服务器已开启" % e)

    def close(self):
        self.sock.close()

    def request(self, **kwargs):
        """
        请求处理中心
        :param kwargs: 
        :return: 
        """
        data = json.dumps({
            'action': kwargs.get('action'),
            'params': kwargs.get('params'),
            'data': kwargs.get('data')
        }).encode("utf-8")

        header = json.dumps({
            'filename': kwargs.get('filename'),
            'filemode': kwargs.get('filemode'),
            'content-length': kwargs.get('filesize', len(data))

        }).encode("utf-8")
        try:
            self.sock.send(struct.pack('i', len(header)))
            self.sock.send(header)
            # 传文件时 忽略首次传递的消息体
            if not kwargs.get('filename'):
                self.sock.sendall(data)
        except ConnectionResetError as e:
            exit("服务器错误：%s，请确认FTP服务器已开启" % e)
        else:
            if kwargs.get('response', True):
                response = json.loads(self.__get_response())
                return response

    def __get_response(self):
        """
        响应处理
        :return: 
        """
        try:
            response = self.sock.recv(4)  # 接收报头长度
            header_length = struct.unpack('i', response)  # 解出报头的长度
            head_info = self.sock.recv(header_length[0])  # 接收报头
            header = json.loads(head_info.decode("utf-8"))  # 解析报头
            content_length = header.get('content-length')
            recv_size = 0
            recv_data = b''  # 数据缓存区
            while recv_size < content_length:
                _content = self.sock.recv(settings.BUFFSIZE)  # 循环接收数据
                if not _content:
                    break
                recv_data += _content
                recv_size += len(_content)

        except ConnectionResetError as e:
            exit("服务器错误：%s，请确认FTP服务器已开启" % e)
        else:
            return recv_data.decode("utf-8")

    def send_file(self, filepath, has_sent=0):
        """
        发送文件
        :param filepath: 
        :param has_sent: 
        :return: 
        """
        total_size = os.path.getsize(filepath)
        data = {
            'action': 'put',
            'filename': os.path.basename(filepath),
            'filesize': total_size,
            'filemd5': FTPService.file_md5(filepath),
            'filemode': 'ab' if has_sent else 'wb',
            'response': False
        }
        self.request(**data)
        try:
            with open(filepath, 'rb') as f:
                f.seek(has_sent)
                while has_sent < total_size:
                    content = f.read(settings.BUFFSIZE)
                    self.sock.sendall(content)
                    has_sent += len(content)
                    FTPService.process_bar(has_sent, total_size)
        except Exception as e:
            exit("服务器错误：%s，请确认FTP服务器已开启" % e)
        else:
            res = json.loads(self.__get_response())
            return res

    def receive_file(self, local_file, remote, filesize, has_recv=0):
        """
        接收文件
        :param local_file:本地文件 
        :param remote: 远程文件
        :param filesize: 远程文件大小
        :param has_recv: 已经接收的大小
        :return: 
        """
        data = {
            'action': 'get',
            'params': {
                'filename': remote,
                'has_recv': has_recv,
            },
            'response': False
        }
        self.request(**data)
        try:
            with open(local_file, 'ab' if has_recv else 'wb') as f:
                f.seek(has_recv)
                while has_recv < filesize:
                    content = self.sock.recv(settings.BUFFSIZE)
                    f.write(content)
                    has_recv += len(content)
                    FTPService.process_bar(has_recv, filesize)
        except Exception as e:
            exit("服务器错误：%s，请确认FTP服务器已开启" % e)
        else:
            res = json.loads(self.__get_response())
            return res

    @staticmethod
    def process_bar(num=1, total=100):
        """
        上传下载的进度条
        :param num: 
        :param total: 
        :return: 
        """
        percent = int(float(num) / float(total) * 100)

        temp = '\r[%s%s]%d %%' % ('#' * percent, '-' * (100 - percent), percent,)
        sys.stdout.write(temp)
        sys.stdout.flush()

    @staticmethod
    def file_md5(filepath):
        """
        文件MD5校验值
        :param filepath: 
        :return: 
        """
        import hashlib
        encrypt = hashlib.md5()
        with open(filepath, 'rb') as f:
            while True:
                b = f.read(8096)
                if not b:
                    break
                encrypt.update(b)
        return encrypt.hexdigest()
