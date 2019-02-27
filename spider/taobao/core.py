#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   core.py
@Desc    :   核心模块：搜索、下载、Cookies
@Contact :   thefreer@outlook.com
@License :   (C)Copyright 2018-2019, TheFreer.NET
@WebSite :   www.thefreer.net
@Modify Time      @Author    @Version
------------      -------    --------
2019/2/27 17:20   thefreer      1.0
'''
import requests
import re
import os
import json
from urllib import parse
import asyncio
import random
from pyppeteer.launcher import launch  # 控制模拟浏览器用
from retrying import retry  #设置重试次数用的

class Searcher():
    def __init__(self, url):
        """
		搜索，得到商品列表
		"""
        ## cookie 和浏览器 UA 是绑定的
        self.headers = {
            "Cookie": "",
            # "Referer": "https://s.taobao.com/search/_____tmd_____/verify/",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:56.0) Gecko/20100101 Firefox/56.0",
            # "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.9 Safari/537.36",
        }
        self.url = url

    def list_parser(self, cookies):
        """
        获取商品列表
        :param cookie:
        :return:
        """
        headers = self.headers
        headers["Cookie"] = cookies
        url = self.url
        try:
            resp = requests.get(url, headers=headers)
        except:
            return []
        html = resp.text
        # print(html)
        page_config = re.findall("g_page_config = {(.*)}", html)
        if len(page_config) != 0:
            js = json.loads("{" + page_config[0] + "}")
            good_list = js['mods']['itemlist']['data']['auctions']
            return good_list
        else:
            return []

    def get_data(self, cookies):
        """
		返回待存入表格的数据
		:return:
		"""
        good_list = self.list_parser(cookies=cookies)
        goods = []
        if len(good_list) >= 10:
            count = 10
        else:
            count = len(good_list)
        for i in range(0, count):
            g = good_list[i]
            # print("===================")
            title = g['raw_title']
            price = g['view_price']
            sales = g['view_sales']
            detail = g['detail_url']
            goods.append((title, price, sales, detail))
        return goods


class Downloader():
    def __init__(self):
        """
		输入一个详情页链接，下载得到所有图片
		"""
        self.headers = {
            "User-Agent":
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36",
        }

    def url_open(self, url):
        """
		处理读入的url,返回html文本
		:param url:
		:return:
		"""
        resp = requests.get(url, headers=self.headers)
        if resp.ok:
            return resp.text

    def down_tm(self, html, name, num):
        """
		获取天猫图片链接
		:param html: 网页源码
		:param name: 命名
		:param num: 图片序号
		:return:
		"""
        i = 0
        bs = re.findall(r'<img src="(.*?)"', html, re.I | re.M)  #正则找到图片链接
        for b in bs:
            i = i + 1
            suffix = re.search(r".(jpg|png|jpeg)(.*).(jpg|png|jpeg)",
                               b).groups()[0]
            tmall_img = 'https:' + re.sub(
                r".(jpg|png|jpeg)(.*).(jpg|png|jpeg)", "", b) + "." + suffix
            image_name = str(name) + '_' + str(i) + '.jpg'
            file_path = 'taobao/%s_%s' % (str(num), str(name))
            f = open(file_path + '/%s_%s' % (str(num), image_name), 'wb')
            res = requests.get(tmall_img)
            for chunk in res.iter_content(chunk_size=20):
                f.write(chunk)
            print('正在下载为: %s 的第 %s 张商品图片' % (name, str(i)))
            print('图片链接为:  %s' % tmall_img)

    def down_tb(self, html, name, num):
        """
		获取淘宝图片链接
		:param html: 网页源码
		:param name: 命名
		:param num: 图片序号
		:return:
		"""
        i = 0
        bs = re.findall(r'<img data-src="(.*?)"', html, re.I | re.M)  #正则找到图片链接
        for b in bs:
            i = i + 1
            suffix = re.search(r".(jpg|png|jpeg)(.*).(jpg|png|jpeg)",
                               b).groups()[0]
            taobao_img = 'https:' + re.sub(
                r".(jpg|png|jpeg)(.*).(jpg|png|jpeg)", "", b) + "." + suffix
            image_name = str(name) + '_' + str(i) + '.jpg'
            file_path = 'taobao/%s_%s' % (str(num), str(name))
            f = open(file_path + '/%s_%s' % (str(num), image_name), 'wb')
            res = requests.get(taobao_img)
            for chunk in res.iter_content(chunk_size=20):
                f.write(chunk)
            print('正在下载标题为: %s 的第 %s 张商品图片' % (name, str(i)))
            print('图片链接为:  %s' % taobao_img)

    # def get_invent(self, html):
    #     inventory = re.findall(r"库存(.*?)", html)[0]
    #     return inventory

    def down_controler(self, url, name, num):
        """
		下载图片顶层模块,先判断链接,再进行爬取
		:param url:
		:param name: 命名
		:param num: 序号
		:return:
		"""
        print("详情页链接为： %s" % url)
        html = self.url_open(url)
        search = re.search('https://detail.tmall.com/', url, re.I | re.M)
        if search:
            self.down_tm(html, name, num)
        else:
            self.down_tb(html, name, num)
        # inventory = self.get_invent(html)
        # return inventory


class Cookier():
    def __init__(self):
        """
		更换cookies
		"""
        self.rtn_cookies = ""
        self.flag = 0

    async def cookie_main(self, url, cookies):
        """
		定义main协程函数，初始化测试环境，主控制
		:param url:
		:param cookies: 待更换的
		:return: 成功则返回新的 cookies， 否则返回 flag 1
		"""
        # 以下使用await 可以针对耗时的操作进行挂起
        browser = await launch({
            'headless': False,
            'args': ['--no-sandbox'],
        })  # 启动pyppeteer 属于内存中实现交互的模拟器
        page = await browser.newPage()  # 启动个新的浏览器页面
        await page.setUserAgent(
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
        )
        await page.setExtraHTTPHeaders({'Cookie': cookies})
        # await page.reload()
        await page.goto(url)  # 访问登录页面
        # 替换淘宝在检测浏览时采集的一些参数。
        # 就是在浏览器运行的时候，始终让window.navigator.webdriver=false
        # navigator是windiw对象的一个属性，同时修改plugins，languages，navigator 且让
        await page.evaluate(
            '''() =>{ Object.defineProperties(navigator,{ webdriver:{ get: () => false } }) }'''
        )  # 以下为插入中间js，将淘宝会为了检测浏览器而调用的js修改其结果。
        await page.evaluate(
            '''() =>{ window.navigator.chrome = { runtime: {},  }; }''')
        await page.evaluate(
            '''() =>{ Object.defineProperty(navigator, 'languages', { get: () => ['en-US', 'en'] }); }'''
        )
        await page.evaluate(
            '''() =>{ Object.defineProperty(navigator, 'plugins', { get: () => [1, 2, 3, 4, 5,6], }); }'''
        )
        # 检测页面是否有滑块。原理是检测页面元素。
        try:
            slider = await page.Jeval('#nocaptcha',
                                      'node => node.style')  # 是否有滑块
        except:
            slider = None
        if slider:
            print('当前页面出现滑块')
            page = await self.mouse_slide(page=page)  # js拉动滑块过去。
            await page.reload()
            self.rtn_cookies = await self.get_cookies(page)  # 导出cookie 完成登陆后就可以拿着cookie玩各种各样的事情了。
            # await page.close()
            return self.rtn_cookies, await page.content()
        else:
            print("当前页面未出现滑块")
            self.flag = 1
            return self.flag

    async def get_cookies(self, page):
        """
		make cookies
		:param page: page 对象
		:param old_cookies: 旧的 cookies
		:return: 返回自己制作的 cookies
		"""
        cookies_list = await page.cookies()
        cookies = ''
        for cookie in cookies_list:
            str_cookie = '{0}={1};'
            if cookie.get('name') == "x5sec":
                str_cookie = str_cookie.format(
                cookie.get('name'), cookie.get('value'))
                cookies += str_cookie
            else:
                pass
        rtn_cookies = "; " + cookies
        # print(cookies)
        return rtn_cookies

    def retry_if_result_none(result):
        return result is None

    @retry(
        retry_on_result=retry_if_result_none, )
    async def mouse_slide(self, page=None):
        """
		鼠标移动到滑块，按下，滑动到头（然后延时处理），松开按键
		:param page:
		:return: 验证成功的 page 对象
		"""
        await asyncio.sleep(2)
        await page.hover('span.btn_slide')  # 不同场景的验证码模块可能名字不同。
        await page.mouse.down()
        # await asyncio.sleep(1)
        await page.mouse.move(
            2000, 2000,
            {'delay': random.randint(400000, 600000)})  # 不同场景的验证码滑动长度和方向可能不同同。
        await page.mouse.up()
        return page


if __name__ == "__main__":

    # os.makedirs('./taobao', exist_ok=True)#总文件夹
    # url = "https://detail.tmall.com/item.htm?spm=a230r.1.14.25.833b388cUyP4PV&id=583768211707&ns=1&abbucket=6"
    # name = "ceshi"
    # tb_downloader = downloader()
    # os.makedirs('./taobao/%s'% str(name), exist_ok=True)#为每个id创建图片文件夹
    # # inventory = tb_downloader.down_controler(url,name)
    # tb_downloader.down_controler(url, name)
    # print('本链接爬取完成, 图片下载完毕')

    os.makedirs('./taobao', exist_ok=True)  #总文件夹
    tb_downloader = Downloader()
    tb_searcher = Searcher()
    keyword = parse.quote("三星 液晶电视 电源板")
    with open('sec_data/cookies.txt', 'r') as c:
        cookie = c.readline()
    for i in range(10):
        goods = tb_searcher.get_data(cookie, keyword)
        print(goods)
        print(len(goods))
    # i = 0
    # for g in goods:
    #     i += 1
    #     url = "https:" +g[3]
    #     name = g[0]
    #     os.makedirs('./taobao/%s_%s'% (str(i), str(name)), exist_ok = True)  # 为每个id创建图片文件夹
    #     # inventory = tb_downloader.down_controler(url,name)
    #     tb_downloader.down_controler(url, name, i)
    #     print('本链接爬取完成, 图片下载完毕')
