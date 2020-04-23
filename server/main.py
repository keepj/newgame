# -*- coding:utf-8 -*-
# @author: luolei
# @file: main.py
# @time: 2019/11/30 2:02
# @description:
import init
import network


def main():
	init.init()
	while True:
		network.run()


if __name__ == "__main__":
	main()
