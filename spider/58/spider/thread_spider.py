#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   thread_spider.py    
@Desc    :   
@Contact :   thefreer@outlook.com
@License :   (C)Copyright 2018-2019, TheFreer.NET
@WebSite :   www.thefreer.net
@Modify Time      @Author    @Version
------------      -------    --------
2019/3/5 13:26   thefreer      1.0         
'''
import requests
from PyQt5 import QtCore
import re
import json
from bs4 import BeautifulSoup
from spider.tools import filter_tags, sleepRandom
from spider.get_mobile import get_mobile, get_driver

# 这个爬虫线程需要扩展为其他爬虫也可以


class driverThread(QtCore.QThread):
    def __init__(self, cookie):
        self.driver = get_driver(cookie)

    def get_driver(self):
        return self.driver


# 1.首先 继承QtCore.QThrea这个类 （这个类中是在按钮点击之后的槽函数进行实例化与运行的）
class spiderThread(QtCore.QThread):
    # 4定义信号参数为str类型
    updata_date = QtCore.pyqtSignal(str)

    # 2进行父类的初始化
    def __init__(self, cookie, driver, url):
        super(spiderThread, self).__init__()
        # 应聘者简历列表url：pageindex表示页数、readflag表示已读未读及全部：0未读、1已读、2全部
        # self.url = 'https://employer.58.com/resume/deliverlist?pageindex={}&readflag=2'
        # self.url = 'https://employer.58.com/resume/recyclelist?pageIndex={}'
        self.url = url
        self.referer = ''
        self.cookie = cookie
        self.driver = driver
        self.headers = {
            'User-Agent':
            'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:64.0) Gecko/20100101 Firefox/64.0',
            'Referer':
            self.referer,
            'Cookie':
            cookie
        }
        self.num = 0
        self.new = 0
        self.fail = 0
        self.old = 0
        self.hs = 0
        self.postDict = {}

    def run(self):
        self.updata_date.emit("爬虫开始......")
        self.listSpider()
        self.updata_date.emit("爬虫结束，共爬取简历信息%d条，新增简历信息 %d 条，重复简历 %d 条，失败简历 %d 条"
                              % (self.num, self.new, self.old, self.fail))
        self.updata_date.emit("finish")

    def listSpider(self, i=1):
        sleepRandom(12)
        url = self.url.format(i)
        headers = self.headers
        headers['Referer'] = url
        resp = requests.get(url=url, headers=headers)
        html = resp.text
        print(html)
        pattern = re.compile(r"\((.*)\)")
        h = re.search(pattern, html).groups(1)[0]
        js = json.loads(h)
        nom = js['data']['resumeList']
        try:
            top = js['data']['topResumeList']
        except:
            top = {}
        if i <= 1:  # 这里加一个判断是为了只爬取加急简历一次，因为每一页都有加急而且都是一样的，所以只爬一遍就够了
            for t in top:
                eUrl = 'https:' + t['url']
                eUrlList = re.split(r'single', eUrl)
                eUrl = eUrlList[0] + 'singles' + eUrlList[1]
                sleepRandom(6)
                EWCList = self.detailSpider(eUrl)
                self.pause(EWCList, t)
        for n in nom:
            eUrl = 'https:' + n['url']
            eUrlList = re.split(r'single', eUrl)
            eUrl = eUrlList[0] + 'singles' + eUrlList[1]
            sleepRandom(6)
            EWCList = self.detailSpider(eUrl)
            self.pause(EWCList, n)
        # 以下代码是一个递归过程，加入nom和top也就是普通和加急都怕爬完了那么这两个就都是空列表那么结束循环，否则继续执行listSpider传入i+1和已经获取的infoList
        if nom == [] and top == []:
            return
        else:
            return self.listSpider(i=i + 1)

    def detailSpider(self, detailUrl):
        # ==================#爬取简历详情页的信息#==================#
        url = detailUrl
        headers = self.headers
        headers['Referer'] = url  # 将headers里的Referer设置为当前要爬取的url
        resp = requests.get(url=url, headers=headers)  # response对象resp
        soup = BeautifulSoup(resp.text, 'lxml')  # beautifulSoup对象soup
        # ==================#解析详情页中的期望地点信息#==================#
        titleItems = soup.select("div.title-content")
        targetLocation = ''
        for item in titleItems:
            if item.find(
                    "div", id="expectLocation"
            ) != None:  # 加一个if是为了防止找不到信息出错，如果找不到targetPosition=''
                targetLocation = item.find(
                    "div", id="expectLocation").text  # 解析到的期望职位
                targetLocation = re.sub(
                    r'\r|\t|\n', '',
                    targetLocation)  # 使用正则表达式去除targetPosition中没有用的空格
        # ==================#解析详情页中的教育信息#==================#
        eduItems = soup.select("div.education ")
        collegeNameList = []  # 用于保存大学名字
        graduateTimeList = []  # 用于保存就读时间
        professionalList = []  # 用于保存专业
        if eduItems != [] and eduItems != None:  # 同样为了防止出错
            collegeNameL = eduItems[0].select(
                "span.college-name")  # 找到存有大学名字的span标签列表
            for collegeN in collegeNameL:  # 一次对span标签列表的标签进行处理
                collegeName = collegeN.text  # 得到单个的大学名
                collegeNameList.append(collegeName)  # 依次将所有大学名存入列表
            # 时间和专业与大学名字原理相同
            graduateTimeL = eduItems[0].select("span.graduate-time")
            for graduateT in graduateTimeL:
                graduateTime = graduateT.text
                graduateTimeList.append(graduateTime)
            professionalL = eduItems[0].select("span.professional")
            for profession in professionalL:
                professional = profession.text
                professionalList.append(professional)
        # 最后将上面解析的学历信息存入一个字典里面
        eduDict = {
            'collegeNameList': collegeNameList,
            'graduateTimeList': graduateTimeList,
            'professionalList': professionalList,
        }
        # ==================#解析详情页中的工作经历信息#==================#
        # 原理同-学历信息
        compItems = soup.select_one("div.work")
        jobTimeList = []  # 工作时间
        compNameList = []  # 公司名字
        jobSalaryList = []  # 工资
        positionList = []  # 职位
        if compItems != None and compItems != []:
            compNameL = compItems.select("div.itemName")
            for com in compNameL:
                compNameList.append(com.text)
            detailContent = compItems.select("div.project-content")
            for con in detailContent:
                spanTag = con.select("span")
                jobTimeList.append(spanTag[0].text)
                jobSalaryList.append(spanTag[1].text)
                positionList.append(spanTag[2].text)

        compDict = {
            'compNameList': compNameList,
            'jobTimeList': jobTimeList,
            'jobSalaryList': jobSalaryList,
            'positionList': positionList,
        }
        # ==================#解析详情页中的获得的证书信息#==================#
        # 原理同学历信息
        certItems = soup.select("div.medal")
        certNameList = []  # 证书名字
        certTimeList = []  # 获取证书时间
        if certItems != [] and certItems != None:
            certNameL = certItems[0].select("span.certificate-name")
            certTimeL = certItems[0].select("span.certificate-time")
            for certN in certNameL:
                certName = certN.text
                certNameList.append(certName)
            for certT in certTimeL:
                certTime = certT.text
                certTimeList.append(certTime)
        certDict = {
            'certNameList': certNameList,
            'certTimeList': certTimeList,
        }
        # ==================#将以上得到的信息存入一个列表里#==================#
        EWCList = [eduDict, certDict, compDict, targetLocation]
        return EWCList  # 函数的返回值为这个信息列表

    def pause(self, EWCList, eDict):
        # # 保密原因 此处代码不方便泄露
        pass

    def getPostData(self, Dict, hs):
        # # 保密原因 此处代码不方便泄露
        pass

    def dataPost(self, Dict, hs):
        # # 保密原因 此处代码不方便泄露
        pass


if __name__ == '__main__':
    url = 'https://employer.58.com/resume/deliverlist?pageindex={}&readflag=2'
    f = open('../cookie.ini', "r")
    cookie = f.readline()
    d = driverThread(cookie)
    t = spiderThread(cookie=cookie, driver=d, url=url)
    t.run()
