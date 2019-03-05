#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   ui_58.py    
@Desc    :   
@Contact :   thefreer@outlook.com
@License :   (C)Copyright 2018-2019, TheFreer.NET
@WebSite :   www.thefreer.net
@Modify Time      @Author    @Version
------------      -------    --------
2019/3/5 13:25   thefreer      1.0         
'''
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QApplication, QMessageBox, QDesktopWidget, QLabel, QComboBox
from PyQt5.QtGui import QIcon
from ui.ui_spider import Ui_MainWindow
import sys
from spider.thread_spider import spiderThread, driverThread


# 这个ui需要改进
class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.beginBtn.clicked.connect(self.spiderStart)
        self.browserBtn.clicked.connect(self.browserStart)
        self.urlList = [
            'https://employer.58.com/resume/deliverlist?pageindex={}&readflag=2',
            'https://employer.58.com/resume/recyclelist?pageIndex={}',
        ]
        self.init_ui()
        self.url = self.urlList[0]

    def init_ui(self):
        self.setWindowTitle("58同城爬虫工具")
        self.setWindowIcon(QIcon('ui/icon.png'))
        self.statusBar().showMessage('Ready')
        choices = ['1. 选择爬取的url', '收到的简历', '回收站']
        self.comboBox.addItems(choices)

    def browserStart(self):
        self.browserBtn.setEnabled(False)
        cookie = self.cookieLine.text()

        #这个ini配置文件需要改进
        if cookie == '' or cookie == None:
            with open('cookie.ini', 'r') as f:
                cookie = f.readlines()[0]
            f.close()
        else:
            with open('cookie.ini', 'w') as f:
                f.write(cookie)
            f.close()
        self.textEdit.append('你输入的cookie为：\n%s\n' % cookie)
        self.driver = driverThread(cookie).get_driver()
        self.cookie = cookie
        self.textEdit.append('PhantomJS启动成功，请点击开始爬取按钮吧！')

    def spiderStart(self):
        if self.comboBox.currentText() == '回收站':
            self.url = self.urlList[1]
        else:
            pass
        self.beginBtn.setEnabled(False)
        self.myThread = spiderThread(self.cookie, self.driver, self.url)
        # 6.接收信号并产生回调函数
        self.myThread.updata_date.connect(self.Display)
        self.myThread.start()

    # 7我是回调函数,显示输出
    def Display(self, data):
        if data == 'finish':
            self.myThread.exit()
            self.beginBtn.setEnabled(True)
        else:
            self.textEdit.append(data)

    def center(self):

        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Message', "确定要退出吗?",
                                     QMessageBox.Yes | QMessageBox.No,
                                     QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())
