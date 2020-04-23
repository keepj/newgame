# -*- coding:utf-8 -*-
# @author: luolei
# @file: C_net.py
# @time: 2019/12/1 22:13
# @description:解压包方法
import struct
import socket


class CPacker(object):
	def __init__(self):
		self.__data = bytes("", encoding="utf-8")

	def pack_char(self, msg):
		# msg = bytes(msg, encoding="utf-8")
		self.__data += struct.pack("b", msg)

	def pack_short(self, msg):
		self.__data += struct.pack("h", socket.htons(msg))

	def pack_int(self, msg):
		self.__data += struct.pack("I", socket.htonl(msg))

	def pack_log(self, msg):
		self.__data += struct.pack("l", socket.htonl(msg))

	def pack_string(self, msg):
		msg = bytes(msg, encoding="utf-8")
		length = len(msg)
		self.__data += struct.pack("I", socket.htonl(length))
		self.__data += struct.pack(str(length) + "s", msg)

	def get_data(self):
		self.__data = struct.pack("I", socket.htonl(len(self.__data))) + self.__data
		return self.__data


class CUnpacker(object):
	def __init__(self, msg):
		self.__data = msg
		self.__msg_cur_offset = 0

	def unpack_char(self):
		msg, = struct.unpack("b", self.__data[self.__msg_cur_offset:self.__msg_cur_offset + 1])
		msg = socket.ntohs(msg)
		self.__msg_cur_offset += 1
		return msg

	def unpack_short(self):
		msg, = struct.unpack("h", self.__data[self.__msg_cur_offset:self.__msg_cur_offset+2])
		msg = socket.ntohs(msg)
		self.__msg_cur_offset += 2
		return msg

	def unpack_int(self):
		msg, = struct.unpack("I", self.__data[self.__msg_cur_offset:self.__msg_cur_offset+4])
		msg = socket.ntohl(msg)
		self.__msg_cur_offset += 4
		return msg

	def unpack_long(self):
		msg, = struct.unpack("l", self.__data[self.__msg_cur_offset:self.__msg_cur_offset+4])
		msg = socket.ntohl(msg)
		self.__msg_cur_offset += 4
		return msg

	def unpack_String(self):
		length = self.unpack_int()
		msg, = struct.unpack(str(length)+"s", self.__data[self.__msg_cur_offset:self.__msg_cur_offset+length])
		self.__msg_cur_offset += length
		msg = str(msg, encoding="utf-8")
		return msg


