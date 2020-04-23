# -*- coding:utf-8 -*-
# @author: luolei
# @file: manager.py
# @time: 2019/11/27 22:10
# @description:处理数据的收发
from .defines import *
from .listener import CListener
from .session import CBaseSession
import handle
import select


class CSessionManager(object):
	def __init__(self):
		self.__Listener = CListener()
		self.__session_dict = {}
		# self.__epoll = select.epoll()

	def get_all_sock(self):
		return self.__session_dict.keys()

	def get_listener(self):
		return self.__Listener

	def Init(self):
		self.__Listener.create_listener(SERVER_IP, SERVER_PORT)
		self.__session_dict[self.__Listener.get_sock_fd()] = self.__Listener
		# self.epoll.register(self.__Listener.get_sock_fd(), select.EPOLLIN | select.EPOLLET)

	def create_session(self, sock, addr):
		sock.setblocking(False)
		sock_fd = sock.fileno()
		session = CBaseSession()
		session.set_sock(sock, addr)
		session.set_connect(True)
		self.__session_dict[sock_fd] = session
		# self.__epoll.register(sock_fd, select.EPOLLIN | select.EPOLLET)

	def del_session(self, fd):
		print("{} 断开连接".format(fd))
		session = self.get_session(fd)
		if session:
			del self.__session_dict[fd]
			session.close()
			# self.__epoll.unregister(fd)

	def get_session(self, fd):
		return self.__session_dict.get(fd)

	# def rcv_all(self):
	# 	# print("开始接受数据 ....")
	# 	listener_fd = self.__Listener.get_sock_fd()
	# 	listener_sock = self.__Listener.get_sock()
	# 	# 未指定超时时间则为阻塞等待, 0.03秒无响应则返回
	# 	epoll_list = self.__epoll.poll(0.03)
	# 	for sock_fd, events in epoll_list:
	# 		if sock_fd == listener_fd:
	# 			new_sock, new_addr = listener_sock.accept()
	# 			self.create_session(new_sock, new_addr)
	# 		elif events & select.EPOLLIN:
	# 			session = self.get_session(sock_fd)
	# 			if session:
	# 				session.rcv_all()
	# 				# 处理缓冲区数据
	# 				while True:
	# 					msg = session.get_next_msg()
	# 					if msg is None:
	# 						break
	# 					else:
	# 						handle.dispatch(sock_fd, msg)
	#
	# 				if not session.get_connect():
	# 					self.del_session(sock_fd)

	def rcv_all(self):
		# print("开始接受数据 ....")
		listener_fd = self.__Listener.get_sock_fd()
		listener_sock = self.__Listener.get_sock()
		# 阻塞等待,最后的参数代表阻塞时间
		readable, writeable, exceptional = select.select(self.__session_dict.keys(), [], [], 2)
		for sock_fd in readable:
			if sock_fd == listener_fd:
				new_sock, new_addr = listener_sock.accept()
				self.create_session(new_sock, new_addr)
			else:
				session = self.get_session(sock_fd)
				if session:
					session.rcv_all()
					# 处理缓冲区数据
					while True:
						msg = session.get_next_msg()
						if msg is None:
							break
						else:
							handle.dispatch(sock_fd, msg)

					if not session.get_connect():
						self.del_session(sock_fd)

	def send_all(self):
		# print("开始发送数据 ....")
		listener_fd = self.__Listener.get_sock_fd()
		for fd, session in self.__session_dict.items():
			if fd == listener_fd:
				continue
			session.send_all()
