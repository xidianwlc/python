#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   tools.py    
@Desc    :   
@Contact :   thefreer@outlook.com
@License :   (C)Copyright 2018-2019, TheFreer.NET
@WebSite :   www.thefreer.net
@Modify Time      @Author    @Version
------------      -------    --------
2019/3/5 13:36   thefreer      1.0         
'''
import re
import random
import time
##过滤HTML中的标签
#将HTML中标签等信息去掉
#@param htmlstr HTML字符串.
def filter_tags(htmlstr):
	#先过滤CDATA
	re_cdata=re.compile('//<!\[CDATA\[[^>]*//\]\]>',re.I) #匹配CDATA
	re_script=re.compile('<\s*script[^>]*>[^<]*<\s*/\s*script\s*>',re.I)#Script
	re_style=re.compile('<\s*style[^>]*>[^<]*<\s*/\s*style\s*>',re.I)#style
	re_br=re.compile('<br\s*?/?>')#处理换行
	re_h=re.compile('</?\w+[^>]*>')#HTML标签
	re_comment=re.compile('<!--[^>]*-->')#HTML注释
	re_all = re.compile('<.*?>')
	s=re_cdata.sub('',htmlstr)#去掉CDATA
	s=re_script.sub('',s) #去掉SCRIPT
	s=re_style.sub('',s)#去掉style
	s=re_br.sub('\n',s)#将br转换为换行
	s=re_h.sub('',s) #去掉HTML 标签
	s=re_comment.sub('',s)#去掉HTML注释
	s=re_all.sub('',s)
	# s=re.sub('\n','',s)
	#去掉多余的空行
	blank_line=re.compile('\n+')
	s=blank_line.sub('\n',s)
	s=replaceCharEntity(s)#替换实体
	return s

##替换常用HTML字符实体.
#使用正常的字符替换HTML中特殊的字符实体.
#你可以添加新的实体字符到CHAR_ENTITIES中,处理更多HTML字符实体.
#@param htmlstr HTML字符串.
def replaceCharEntity(htmlstr):
	CHAR_ENTITIES={'nbsp':' ','160':' ',
				'lt':'<','60':'<',
				'gt':'>','62':'>',
				'amp':'&','38':'&',
				'quot':'"','34':'"',}

	re_charEntity=re.compile(r'&#?(?P<name>\w+);')
	sz=re_charEntity.search(htmlstr)
	while sz:
		entity=sz.group()#entity全称，如&gt;
		key=sz.group('name')#去除&;后entity,如&gt;为gt
		try:
			htmlstr=re_charEntity.sub(CHAR_ENTITIES[key],htmlstr,1)
			sz=re_charEntity.search(htmlstr)
		except KeyError:
			#以空串代替
			htmlstr=re_charEntity.sub('',htmlstr,1)
			sz=re_charEntity.search(htmlstr)
	return htmlstr

def repalce(s,re_exp,repl_string):
	return re_exp.sub(repl_string,s)

def charParse(uChar):
	pattern = re.compile(u'[\u4E00-\u9FA5]')
	if re.search(pattern, uChar):#非中文
		char = str(uChar.encode('utf-8'))[2:][: -1]
		char = re.sub(r"\\x", '%', char).upper()
		return char
	else:
		return uChar

def sleepRandom(t):
	sleep = random.randint(t, t+random.randint(2, 7))
	time.sleep(sleep)
	# pass
