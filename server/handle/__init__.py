# -*- coding:utf-8 -*-
# @author: luolei
# @file: handle.py
# @time: 2019/12/5 0:28
# @description:分发接受数据
import network
from .handlereceive import FUNC_DICT
from .handlesend import *


def dispatch(sock_fd, msg):
	unpacker = network.C_net.CUnpacker(msg)
	msg_id = unpacker.unpack_int()
	if msg_id in FUNC_DICT:
		msg = msg[4:]
		for sock_fd in network.g_session_manager.get_all_sock():
			if sock_fd == network.g_session_manager.get_listener().get_sock_fd():
				continue
			FUNC_DICT[msg_id](sock_fd, msg)



