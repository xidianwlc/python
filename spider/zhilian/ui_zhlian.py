#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   ui_zhlian.py    
@Desc    :   
@Contact :   thefreer@outlook.com
@License :   (C)Copyright 2018-2019, TheFreer.NET
@WebSite :   www.thefreer.net
@Modify Time      @Author    @Version
------------      -------    --------
2019/3/5 13:37   thefreer      1.0         
'''
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QApplication, QMessageBox, QDesktopWidget, QLabel, QComboBox
from PyQt5.QtGui import QIcon
from ui.ui_spider import Ui_MainWindow
import sys
from spider.thread_spider import spiderThread
import time


# 这个ui需要改进
class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
	def __init__(self, parent=None):
		super(MainWindow, self).__init__(parent)
		self.setupUi(self)
		self.beginBtn.clicked.connect(self.spiderStart)
		self.endBtn.clicked.connect(self.spiderEnd)
		self.init_ui()
	
	def init_ui(self):
		self.setWindowTitle("智联招聘爬虫工具")
		self.setWindowIcon(QIcon('ui/icon.png'))
		self.statusBar().showMessage('Ready')
	
	# choices = ['1. 选择爬取的url', '收到的简历', '回收站']
	# self.comboBox.addItems(choices)
	
	def spiderEnd(self):
		self.myThread.exit()
		self.textEdit.append("爬虫线程被手动终结")
		self.beginBtn.setEnabled(True)
	
	def spiderStart(self):
		self.beginBtn.setEnabled(False)
		cookie = self.cookieLine.text()
		if cookie == '' or cookie == None:
			with open('cookie.ini', 'r') as f:
				cookie = f.readlines()[0]
			f.close()
		else:
			with open('cookie.ini', 'w') as f:
				f.write(cookie)
			f.close()
		self.textEdit.append('你输入的cookie为：\n%s\n' % cookie)
		self.textEdit.append('起始数字为 ：%s' % startNum)
		self.cookie = cookie
		self.startNum = startNum
		self.myThread = spiderThread( self.cookie, self.startNum)
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
		reply = QMessageBox.question(self, 'Message', "确定要退出吗?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
		
		if reply == QMessageBox.Yes:
			event.accept()
		else:
			event.ignore()


if __name__ == '__main__':
	app = QApplication(sys.argv)
	win = MainWindow()
	win.show()
	sys.exit(app.exec_())
