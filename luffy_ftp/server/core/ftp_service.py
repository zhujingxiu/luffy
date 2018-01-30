#!/usr/bin/env python
# -*- coding:utf-8 -*-
# _AUTHOR_  : zhujingxiu
# _DATE_    : 2018/1/29
import os
import platform
import socket
import json
import struct
from .auth import Auth
from conf import settings
from core import utils


class FTPService:
    def __init__(self):
        self.conn = None
        self.addr = None
        self.username = None
        self.home_dir = None
        self.current_path = ""
        self.user_quota = 0
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind(settings.ADDRESS)
        self.sock.listen(settings.LISTEN_LIMIT)

    def __send_response(self, data):
        """
        发送处理结果
        :param data: 
        :return: 
        """

        code = data.get('errorno', 0) if isinstance(data, dict) else int(data)
        result = {
            'errorno': code,
            'errormsg': FTPService.error_msg(code),
            'data': data.get('data', '') if isinstance(data, dict) else ''
        }
        result_bytes = json.dumps(result).encode("utf-8")
        header = json.dumps({
            'content-length': len(result_bytes)
        }).encode("utf-8")
        self.conn.send(struct.pack('i', len(header)))
        self.conn.send(header)
        self.conn.sendall(result_bytes)

    def __parse_request(self):
        """
        解析请求数据
        :return: 
        """

        response = self.conn.recv(4)  # 接收报头长度
        if not response:
            return False
        header_length = struct.unpack('i', response)  # 解出报头的长度
        head_info = self.conn.recv(header_length[0])  # 接收报头
        header = json.loads(head_info)  # 解析报头
        content_length = header.get('content-length')
        filename = header.get('filename')
        filemode = header.get('filemode')
        # 开始收数据
        recv_size = 0
        recv_data = b''
        # 接收文件
        if filename and filemode:
            fh = open(os.path.join(self.current_path, filename), filemode)
        while recv_size < content_length:
            if content_length - recv_size < settings.BUFFSIZE:
                _size = content_length - recv_size
            else:
                _size = settings.BUFFSIZE
            content = self.conn.recv(_size)
            recv_size += len(content)
            if filename and filemode:
                fh.write(content)
            else:
                recv_data += content

        if filename and filemode:
            fh.close()
            return {'action': header.get('action', 'put'),
                    'params': {'received': True, 'filename': filename, 'filesize': recv_size,
                               'filemd5': header.get('filemd5')}}
        else:
            return json.loads(recv_data.decode('utf-8'))

    def run(self):
        """
        FTP服务入口
        :return: 
        """
        print("服务已启动 %s:%s..." % (settings.HOST, settings.PORT))
        while True:
            try:
                self.conn, self.addr = self.sock.accept()
                print("来自[%s]的新的请求" % (self.addr,))
                self.__dispatch()
            except Exception as e:
                print("连接异常：%s" % e)

    def __dispatch(self):
        """
        客户端请求分发
        :return: 
        """
        while True:
            request = self.__parse_request()
            if not isinstance(request,dict):
                return False
            action = request.get('action')
            params = request.get('params')
            if not action:
                return 99
            action = "_%s__%s" % (self.__class__.__name__, action)  # 私有成员方法的访问
            if hasattr(self, action):
                data = getattr(self, action)(**params)
            else:
                data = 1
            self.__send_response(data)

    def __client_path(self, path):
        """
        客户端绝对路径和相对路径
        :param path: 
        :return: 
        """
        return {
            'abspath': os.path.abspath(path),
            'relpath': "~" if path == self.home_dir else os.path.relpath(path, self.home_dir)
        }

    def __os_info(self):
        """
        服务器信息
        :return: 
        """
        return {
            'hostname': socket.gethostname(),
            'address': self.conn.getpeername(),
        }

    def __auth(self, **kwargs):
        """
        用户登录验证
        :param kwargs: 
        :return: 
        """
        username = kwargs.get('username')
        password = kwargs.get('password')
        if not username or not password:
            return 99
        user_auth = Auth()
        result = user_auth.authentication(username, password)
        if not result:
            return 98
        self.username = result.get('username')
        self.user_quota = result.get('quota')
        self.home_dir = result.get('home_dir')
        self.current_path = self.home_dir
        info = self.__os_info()
        info.update(self.__client_path(self.home_dir))
        return {'data': info}

    def __ls(self, **kwargs):
        """
        查看目录列表
        :param kwargs: 
        :return: 
        """
        path = kwargs.get('path', '')
        full_path = os.path.abspath(os.path.join(self.current_path, path))
        if not full_path.startswith(self.home_dir):
            return 97
        if not os.path.exists(full_path):
            return 96
        if platform.system().lower() == 'windows':
            cmd = 'dir'
        else:
            cmd = 'ls'
        res = os.popen('%s %s' % (cmd, full_path)).read()

        return {'data': res}

    def __pwd(self, **kwargs):
        """
        客户端当前相对路径
        :param kwargs: 
        :return: 
        """
        abs_path = kwargs.get('path', '')
        return {'data': os.path.relpath(abs_path, settings.BASE_DIR)}

    def __mkdir(self, **kwargs):
        """
        客户端创建文件夹
        :param kwargs: 
        :return: 
        """
        path = kwargs.get('path', '')
        full_path = os.path.abspath(os.path.join(self.current_path, path))
        if not full_path.startswith(self.home_dir):
            return 97
        res = os.popen('mkdir %s' % full_path).read()
        return {'data': res}

    def __cd(self, **kwargs):
        """
        客户端切换目录
        :param kwargs: 
        :return: 
        """
        path = kwargs.get('path', '')
        full_path = os.path.abspath(os.path.join(self.current_path, path))

        if not full_path.startswith(self.home_dir):
            return 97
        if not os.path.exists(full_path):
            return 96

        res = os.popen('cd %s' % full_path).read()
        if not res:
            self.current_path = full_path
            result = self.__client_path(full_path)
        else:
            result = res

        return {'data': result}

    def __user_available(self):
        """
        客户端家目录可用大小
        :param kwargs: 
        :return: 
        """
        used_size = utils.dir_used(self.home_dir)
        return self.user_quota - used_size

    def __put(self, **kwargs):
        """
        客户端上传文件
            filename 文件名
            filemode 文件打开模式
            filesize 文件总大小
            received 已接受大小
            filemd5 文件md5校验值
        :param kwargs: 
        :return: 
        """
        filename = kwargs.get('filename')
        filemode = kwargs.get('filemode', '')
        filesize = kwargs.get('filesize')
        received = kwargs.get('received', False)
        filemd5 = kwargs.get('filemd5', None)
        filepath = os.path.join(self.current_path, filename)
        has_sent = 0
        if os.path.exists(filepath):
            has_sent = os.path.getsize(filepath)
        if self.__user_available() < filesize - has_sent:
            return 95
        if not filemode:
            return {'data': {'has_sent': has_sent}}
        if received and utils.file_md5(filepath) != filemd5:
            return 94

        return {'data': {'filepath': filepath}}

    def __get(self, **kwargs):
        """
        客户端下载文件
        :param kwargs: 
        :return: 
        """
        filename = kwargs.get('filename')
        has_recv = kwargs.get('has_recv', -1)
        filepath = os.path.join(self.current_path, filename)
        filesize = os.path.getsize(filepath)
        if not os.path.exists(filepath):
            return 96

        if has_recv < 0:
            return {'data': {
                'filename': os.path.basename(filename),
                'filemd5': utils.file_md5(filepath),
                'filesize': filesize}
            }
        with open(filepath, 'rb') as f:
            f.seek(has_recv)
            while has_recv < filesize:
                content = f.read(settings.BUFFSIZE)
                self.conn.sendall(content)
                has_recv += len(content)
        if has_recv == filesize:
            print("文件传输完毕")
        return {'data': ''}

    @staticmethod
    def error_msg(errorno):
        """
        错误消息处理中心
        :param errorno: 
        :return: 
        """
        msg = {
            0: 'success',
            1: '语法错误',
            94: '文件md5校验失败',
            95: '空间不足',
            96: '文件或目录不存在',
            97: '权限不足',
            98: '用户验证失败',
            99: '参数异常',
        }
        return "\033[91m%s\033[0m" % msg.get(errorno, '未知错误')
