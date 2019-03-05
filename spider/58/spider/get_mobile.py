#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   get_mobile.py    
@Desc    :   
@Contact :   thefreer@outlook.com
@License :   (C)Copyright 2018-2019, TheFreer.NET
@WebSite :   www.thefreer.net
@Modify Time      @Author    @Version
------------      -------    --------
2019/3/5 13:26   thefreer      1.0         
'''
import base64
from fontTools.ttLib import TTFont, BytesIO
import re
from selenium import webdriver
import time
posi_dict = {
	'" xMin="91" yMin="-26" xMax="1113" yMax="1575': 0,
	'" xMin="212" yMin="0" xMax="764" yMax="1583': 1,
	'" xMin="119" yMin="0" xMax="1093" yMax="1575': 2,
	'" xMin="143" yMin="-26" xMax="1049" yMax="1575': 3,
	'" xMin="17" yMin="0" xMax="1162" yMax="1549': 4,
	'" xMin="174" yMin="-27" xMax="1054" yMax="1549': 5,
	'" xMin="118" yMin="-26" xMax="1115" yMax="1575': 6,
	'" xMin="111" yMin="0" xMax="1095" yMax="1549': 7,
	'" xMin="98" yMin="-25" xMax="1103" yMax="1575': 8,
	'" xMin="100" yMin="-26" xMax="1094" yMax="1575': 9,
}
def get_driver(cookie):
	pattern = re.compile(r'(.*?)=(.*?);')
	cook = re.findall(pattern, cookie)
	cookies = {}
	for c in cook:
		cookies[str(c[0])] = c[1]
	driver = webdriver.PhantomJS()
	driver.get('https://employer.58.com/')
	driver.delete_all_cookies()
	for c in cookies:
		try:
			driver.add_cookie({'name': str(c), 'value': str(cookies[c])})
		except:
			pass
	time.sleep(1)
	driver.refresh()
	return driver
def get_secure_code(url, driver):
	driver.get(url)
	time.sleep(1)
	script = 'console.log(window.____global.pageJson.phoneProtect.number);'
	driver.execute_script(script)
	secCode = list(driver.get_log('browser'))[0]['message']
	html = driver.page_source
	basrStr = re.search(r'src:url\(data:application/font-woff;charset=utf-8;base64,(.*?)\)', html).groups()[0]
	return secCode, basrStr

def make_font_file(base64_string: str):
	bin_data = base64.decodebytes(base64_string.encode())
	with open('./58tmp.woff', "wb") as f:
		f.write(bin_data)
	return bin_data
def convert_font_to_xml(bin_data):
	font = TTFont(BytesIO(bin_data))
	font.saveXML('./58tmp.xml')

def get_number_dict(base_str, code):
	convert_font_to_xml(make_font_file(base_str))
	name_dict = {}
	font_dict = {}
	font_list = []
	lines = ''
	sec_code = re.sub(r'&#', '0', code)
	code_list = re.split(r';', sec_code)[:-1]
	#得到所有键值对
	with open('./58tmp.xml', 'r', encoding='UTF-8') as f:
		line = f.readlines()
		line = str(line)
		while line:
			lines += line
			content = re.findall(r'code="([^"]*?)" name="([^"]*?)"', line)
			if content:
				font_list = content
			line = f.readlines()

	#得到name字典
	for font in font_list:
		if font[0] in code_list:
			name_dict[font[0]] = font[1]

	# 得到数字坐标信息
	for key in name_dict:
		cmp = re.search(r'<TTGlyph name="' + name_dict[key] + '(.*?)">', lines)
		font_dict[key] = cmp.groups()[0]
	return font_dict, code_list

def get_mobile(url, driver):
	sec_code, base_str = get_secure_code(url, driver)
	font_dict, code_list = get_number_dict(base_str, sec_code)
	mobile = ''
	for code in code_list:
		pos = font_dict[code]
		if pos in posi_dict:
			mobile += str(posi_dict[pos])
	return mobile

if __name__ == '__main__':
	url = ""
	cookie = ""
	driver = get_driver(cookie)
	mobile = get_mobile(url, driver=driver)
	print(mobile)




