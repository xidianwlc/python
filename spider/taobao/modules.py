#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   modules.py    
@Contact :   thefreer@outlook.com
@License :   (C)Copyright 2018-2019, TheFreer.NET
@WebSite :   www.thefreer.net
@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2019/2/27 17:22   thefreer      1.0         工具模块
'''
import re
import random
import xlwt
import time
import pandas as pd

def keywords_reader(excel):
	"""
	读取一个文件里的所有 关键字
	:param excel:
	:return: 关键字列表
	"""

def cookie_replace(cookies_list, old_cookies):
	"""
	一个 cookie 爬 100 个关键字就更换另一个 cookie
	:param cookies_list:
	:return:
	"""
	new_cookies = cookies_list.pop()
	cookies_list.append(old_cookies)
	return new_cookies

def excel_spilt(excel):
	"""
	分割一个表格为行数为 100 的若干个表格
	:param excel:
	:return:
	"""
	df = pd.read_excel(r'excels/康佳 灯条.xlsx')
	df2 = df[df.duplicated('种类') == False]['种类']
	for i in df2:
		df3 = df[df['种类'] == i]
		df3.to_excel(r'excels/spilts/%s.xls' % i)

def data_to_excel(goods):
	"""
	数据存入 excel
	:param goods:
	:return:
	"""
	pass

def sleepRandom(t):
	"""
	睡眠随机时长
	:param t:
	:return:
	"""
	sleep = random.randint(t, t+random.randint(1, 4))
	# sleep = 1
	time.sleep(sleep)

if __name__ == '__main__':
	keywords = keywords_reader()
	print(keywords)
	print(len(keywords))