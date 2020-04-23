# -*- coding:utf-8 -*-
# @author: luolei
# @file: hallsessionmanager.py
# @time: 2019/12/5 0:15
# @description:接受客户端信息
from network.manager import CSessionManager


class CHallSessionManager(CSessionManager):
	def __init__(self):
		super(CHallSessionManager, self).__init__()
		self.m_FuncDict = {}

	def register(self, msg_id, func):
		if msg_id in func:
			raise Exception("协议id 0x{:x} 已经存在,注册失败".format(msg_id))
		self.m_FuncDict[msg_id] = func

	def dispatch(self, msg):
		pass
