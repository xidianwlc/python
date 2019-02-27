#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   main.py
@Desc:   :   主控制模块
@Contact :   thefreer@outlook.com
@License :   (C)Copyright 2018-2019, TheFreer.NET
@WebSite :   www.thefreer.net
@Modify Time      @Author    @Version
------------      -------    --------
2019/2/27 19:12   thefreer      1.0
'''
from urllib import parse
import asyncio
import re
import time
from core import Searcher, Cookier
from modules import cookie_replace

keyword = parse.quote("三星 液晶电视 主板")
url = "https://s.taobao.com/search?q=%s&sort=sale-desc" % keyword
with open('sec_data/cookies.txt', 'r') as f:
    ori_cookies = re.sub("; x5sec=(.*)", "", f.readline())
searchr = Searcher(url=url)
cookier = Cookier()
use_cookies = ori_cookies
limit = 0
while True:
    limit += 1
    if limit <= 20:
        goods = searchr.get_data(cookies=use_cookies)
        time.sleep(1)
        if len(goods) == 0:
            try:
                loop = asyncio.get_event_loop(
                )  # 协程，开启个无限循环的程序流程，把一些函数注册到事件循环上。当满足事件发生的时候，调用相应的协程函数。
                new_cookies, html = loop.run_until_complete(
                    cookier.cookie_main(url=url,
                                        cookies=use_cookies))  # 将协程注册到事件循环，并启动事件循环
                if re.search(r"刷新", html):
                    print("此 Cookies 过度使用，为了可持续发展，将更换 Cookies...")
                    cookie_replace([], ori_cookies)
                    break
                elif re.search(r"通过", html):
                    loop.stop()
                    print("验证通过...")
                    use_cookies = ori_cookies + new_cookies
                else:
                    print("未知错误，停止运行...")
            except:
                pass
        else:
            pass
