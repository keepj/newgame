# -*- coding:utf-8 -*-
# @author: luolei
# @file: handlesend.py
# @time: 2019/12/15 22:48
# @description:发送数据处理
from network import C_net
import network


def GS2CChat(sock_fd, msg):
	packer = C_net.CPacker()
	packer.pack_int(0x01)
	packer.pack_char(1)
	packer.pack_short(2)
	packer.pack_int(10)
	packer.pack_log(10000)
	packer.pack_string(msg)
	network.send_msg(sock_fd, packer.get_data())
	print("GS2CChat = {}".format(msg))

