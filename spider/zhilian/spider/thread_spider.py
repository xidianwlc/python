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
2019/3/5 13:35   thefreer      1.0         
'''
import requests
from PyQt5 import QtCore
import re
import json
import time
import random
from spider.tools import filter_tags, sleepRandom
import logging

### 加一个日志功能

ranNumList = [0]  # 随机数要用到


# 1.首先 继承QtCore.QThrea这个类 （这个类中是在按钮点击之后的槽函数进行实例化与运行的）
class spiderThread(QtCore.QThread):
    # 4定义信号参数为str类型
    updata_date = QtCore.pyqtSignal(str)

    # 2进行父类的初始化
    def __init__(self, cookie, startNum):
        super(spiderThread, self).__init__()
        # 应聘者简历列表url：pageindex表示页数、readflag表示已读未读及全部：0未读、1已读、2全部
        # self.url = 'https://employer.58.com/resume/deliverlist?pageindex={}&readflag=2'
        # self.url = 'https://employer.58.com/resume/recyclelist?pageIndex={}'
        self.url = 'https://ihr.zhaopin.com/resumemanage/resumelistbykey.do'
        self.cookie = cookie
        self.startNum = startNum
        self.headers = {
            'User-Agent':
            'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:64.0) Gecko/20100101 Firefox/64.0',
            'Referer':
            'https://ihr.zhaopin.com/resume/manage/',
            'Cookie':
            cookie,
        }
        self.postData = {
            'startNum': self.startNum,
            'rowsCount': '30',
            'ageStart': '',
            'ageEnd': '',
            'workYears': '',
            'sex': '',
            'edu': '',
            'liveCity': '',
            'hopeWorkCity': '',
            'upDate': '',
            'companyName': '',
            'exclude': '',
            'keywords': '',
            'onlyLastWork': 'false',
            'orderFlag': 'commu',
            'countFlag': '1',
            'jobNo': '',
            'pageType': 'all',
            'source': '1;2;5',
            'sort': 'status'
        }
        self.num = 0 + self.startNum
        self.new = 0
        self.fail = 0
        self.old = 0
        self.hs = 0
        self.postDict = {}
        self.resumeList = []

    def run(self):
        # self.updata_date.emit("爬虫开始......")
        self.listSpider()
        print(len(self.resumeList))

    # self.updata_date.emit("爬虫结束，共爬取简历信息%d条，新增简历信息 %d 条，重复简历 %d 条，失败简历 %d 条"%(self.num, self.new, self.old, self.fail))
    # self.updata_date.emit("finish")

    def listSpider(self):
        self.postData['startNum'] = self.startNum
        resp = requests.post(
            self.url, headers=self.headers, data=self.postData)
        html = resp.text
        js = json.loads(html)
        self.resumeList = js['data']['commu']['results']
        sleepRandom(3)
        for resume in self.resumeList:
            sleepRandom(1)
            id = resume['id']
            jobNumber = resume['jobNumber']
            number = resume['number']
            resumeSource = resume['resumeSource']
            version = resume['version']
            durl = 'https://ihr.zhaopin.com/resumesearch/getresumedetial.do?resumeNo=%s_%s_%s_%s_%s&resumeSource=10' % (
                str(id), str(jobNumber), str(number), str(resumeSource),
                str(version))
            EWCList = self.detailSpider(detailUrl=durl)
            self.pause(ewc=EWCList, info=resume)
        if len(self.resumeList) == 0:
            return
        else:
            self.startNum += 100
            return self.listSpider()

    def detailSpider(self, detailUrl):
        resp = requests.get(detailUrl, headers=self.headers)
        html = resp.text
        js = json.loads(html)
        info = dict(js['data'])
        # print(info['detialJSonStr'])
        detailInfo = json.loads(info['detialJSonStr'])
        # userDetail = info['userDetials']
        collegeNameList = []  # 用于保存大学名字
        graduateTimeList = []  # 用于保存就读时间
        professionalList = []  # 用于保存专业
        eduList = list(detailInfo['EducationExperience'])
        if eduList:
            for edu in eduList:
                collegeName = edu['SchoolName']
                graduateTime = edu['DateStart'] + " - " + edu['DateEnd']
                professional = edu['MajorName']
                collegeNameList.append(collegeName)
                graduateTimeList.append(graduateTime)
                professionalList.append(professional)
        eduDict = {
            'collegeNameList': collegeNameList,
            'graduateTimeList': graduateTimeList,
            'professionalList': professionalList,
        }

        jobTimeList = []  # 工作时间
        compNameList = []  # 公司名字
        jobSalaryList = []  # 工资
        positionList = []  # 职位
        workList = list(detailInfo['WorkExperience'])
        if workList:
            for work in workList:
                jobTime = work['DateStart'] + " - " + work['DateEnd']
                compName = work['CompanyName']
                salary = work['Salary']
                lens = len(salary)
                jobSalary = salary[:int(lens /
                                        2)] + "元-" + salary[int(lens / 2) +
                                                            1:] + "元"
                position = work['JobTitle']
                jobTimeList.append(jobTime)
                compNameList.append(compName)
                jobSalaryList.append(jobSalary)
                positionList.append(position)
        workDict = {
            'compNameList': compNameList,
            'jobTimeList': jobTimeList,
            'jobSalaryList': jobSalaryList,
            'positionList': positionList,
        }
        certNameList = []  # 证书名字
        certTimeList = []  # 获取证书时间
        certList = list(detailInfo['AchieveCertificate'])
        if certList:
            for cert in certList:
                certName = cert['CertificateName']
                certTime = cert['AchieveDate']
                certNameList.append(certName)
                certTimeList.append(certTime)
        certDict = {
            'certNameList': certNameList,
            'certTimeList': certTimeList,
        }
        try:
            zwpj = detailInfo['CommentContent']
        except:
            zwpj = ""
        # ==================#将以上得到的信息存入一个列表里#==================#
        EWCList = [eduDict, certDict, workDict, zwpj]
        return EWCList

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
    with open('../cookie.ini', 'r') as c:
        cookie = c.readline()
    spider = spiderThread(cookie, 162)
    spider.run()
