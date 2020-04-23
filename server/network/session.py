# -*- coding:utf-8 -*-
# @author: luolei
# @file: listener.py
# @time: 2019/11/7 22:56
# @description: 发起连接
import socket
import struct
import errno
from .buffer import CBuffer


class CBaseSession(object):
	def __init__(self):
		self.__sock = None
		self.__addr = None
		self.rcv_buffer = CBuffer()
		self.send_buffer = CBuffer()
		self.connect_flag = False
		self.connect_cnt = 5

	def set_sock(self, sock, addr):
		self.__sock = sock
		self.__addr = addr

	def get_sock(self):
		return self.__sock

	def get_connect(self):
		return self.connect_flag

	def set_connect(self, flag):
		self.connect_flag = flag

	def connect(self, ip, port):
		if self.connect_cnt <= 0:
			print("超过最大连接次数")
			self.__sock.close()
			return False
		try:
			self.__sock.connect((ip, port))
			self.connect_cnt = 5
			self.connect_flag = True
			return True
		except:
			self.connect_cnt -= 1
			self.connect()

	def close(self):
		self.__sock.close()

	def rcv_msg(self, msg):
		self.rcv_buffer.push(msg)

	def send_msg(self, msg):
		self.send_buffer.push(msg)

	def dispatch(self, msg):
		pass

	def get_next_msg(self):
		msg_header = self.rcv_buffer.peek(4)
		if msg_header is None or len(msg_header) != 4:
			return None

		msg_len, = struct.unpack("I", msg_header)
		msg_len = socket.ntohl(msg_len)
		msg_len += 4
		buff_size = self.rcv_buffer.get_data_len()
		if buff_size < msg_len:
			return None
		msg = self.rcv_buffer.pop(msg_len)
		return msg[4:]

	def rcv_all(self):
		# 先将所有的数据放入缓冲区
		while True:
			try:
				msg = self.__sock.recv(4096 * 4)
				if len(msg) > 0:
					self.rcv_msg(msg)
				else:
					self.set_connect(False)
					return
			except socket.error as e:
				if e.errno == errno.ECONNRESET:
					self.set_connect(False)
				return

	def send_all(self):
		if not self.get_connect():
			return

		while True:
			data = self.send_buffer.peek(4096 * 4)
			if data is None:
				return
			data_len = self.__sock.send(data)
			# 更新偏移量
			if data_len > 0:
				self.send_buffer.update_offset(data_len)
			else:
				return
