# -*- coding:utf-8 -*-
# @author: luolei
# @file: buffer.py
# @time: 2019/11/24 17:44
# @description:数据缓冲


class CBuffer(object):
	def __init__(self):
		self.__data = bytes("", encoding="utf-8")

	def push(self, data):
		self.__data += data

	# 接受数据时使用
	def pop(self, data_len):
		if len(self.__data) < data_len:
			return None

		data = self.__data[:data_len]
		self.__data = self.__data[data_len:]
		return data

	# 发送数据时使用
	def peek(self, data_len):
		if len(self.__data) == 0:
			return None

		if len(self.__data) < data_len:
			data_len = len(self.__data)

		data = self.__data[:data_len]
		return data

	def update_offset(self, data_len):
		if len(self.__data) < data_len:
			self.__data = ""
		else:
			self.__data = self.__data[data_len:]

	def clear(self):
		self.__data = ""

	def get_data_len(self):
		return len(self.__data)
