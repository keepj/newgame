# -*- coding:utf-8 -*-
# -*- coding:utf-8 -*-
# @author: luolei
# @file: __init__.py
# @time: 2019/11/7 22:56
# @description:
from .manager import CSessionManager


def my_init():
	global g_session_manager
	g_session_manager = CSessionManager()
	g_session_manager.Init()


def run():
	global g_session_manager
	if not g_session_manager:
		return
	g_session_manager.rcv_all()
	g_session_manager.send_all()


# 将数据压入缓冲区，并未真正发送
def send_msg(fd, msg):
	global g_session_manager
	if not g_session_manager:
		return
	session = g_session_manager.get_session(fd)
	if not session:
		return
	session.send_msg(msg)
