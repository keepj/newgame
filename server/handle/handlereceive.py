# -*- coding:utf-8 -*-
# @author: luolei
# @file: handlereceive.py
# @time: 2019/12/15 22:49
# @description:接受数据处理
from network import C_net
from .handlesend import GS2CChat


def C2GSChat(sock_fd, msg):
	unpacker = C_net.CUnpacker(msg)
	a = unpacker.unpack_char()
	b = unpacker.unpack_short()
	c = unpacker.unpack_int()
	d = unpacker.unpack_long()
	msg = unpacker.unpack_String()
	print("C2GSChat = {} {} {} {} {}".format(msg, a, b, c, d))
	GS2CChat(sock_fd, msg)

FUNC_DICT = {
	0x01: C2GSChat,
}
