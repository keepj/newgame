# -*- coding:utf-8 -*-
# @author: luolei
# @file: listener.py
# @time: 2019/11/7 22:56
# @description: 接受连接
from .buffer import CBuffer
import socket


class CListener(object):
	def __init__(self):
		self.__sock = None
		self.__ip = None
		self.__port = None
		self.__rcv_buffer = CBuffer()
		self.__send_buffer = CBuffer()

	def create_listener(self, ip, port):
		if not (ip and port):
			print("请检查IP和端口配置")
			return

		self.__ip = ip
		self.__port = port
		# 创建套接字
		self.__sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.__sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # 允许地址复用
		self.__sock.setblocking(False)  # 设置为非阻塞态
		self.__sock.bind((ip, port))
		self.__sock.listen(5)

	def get_sock(self):
		return self.__sock

	def get_sock_fd(self):
		return self.__sock.fileno()
