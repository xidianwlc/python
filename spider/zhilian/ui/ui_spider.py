# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_spider.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(692, 570)
        MainWindow.setStyleSheet("")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.beginBtn = QtWidgets.QPushButton(self.centralwidget)
        self.beginBtn.setGeometry(QtCore.QRect(490, 400, 161, 51))
        self.beginBtn.setStyleSheet("background-color: rgb(0, 255, 127);\n"
"font: 75 14pt \"微软雅黑\";")
        self.beginBtn.setObjectName("beginBtn")
        self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit.setGeometry(QtCore.QRect(30, 40, 621, 341))
        self.textEdit.setStyleSheet("background-color: rgb(170, 170, 127);\n"
"font: 11pt \"微软雅黑\";\n"
"border-color: rgb(0, 0, 0);")
        self.textEdit.setObjectName("textEdit")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(10, 10, 61, 20))
        self.label.setStyleSheet("font: 75 11pt \"微软雅黑\";")
        self.label.setObjectName("label")
        self.cookieLine = QtWidgets.QLineEdit(self.centralwidget)
        self.cookieLine.setGeometry(QtCore.QRect(40, 450, 211, 41))
        self.cookieLine.setStyleSheet("font: 11pt \"微软雅黑\";")
        self.cookieLine.setText("")
        self.cookieLine.setObjectName("cookieLine")
        self.cookieLabel = QtWidgets.QLabel(self.centralwidget)
        self.cookieLabel.setGeometry(QtCore.QRect(60, 400, 151, 20))
        self.cookieLabel.setStyleSheet("font: 75 11pt \"微软雅黑\";")
        self.cookieLabel.setObjectName("cookieLabel")
        self.cookieLabel_2 = QtWidgets.QLabel(self.centralwidget)
        self.cookieLabel_2.setGeometry(QtCore.QRect(310, 400, 121, 20))
        self.cookieLabel_2.setStyleSheet("font: 75 11pt \"微软雅黑\";")
        self.cookieLabel_2.setObjectName("cookieLabel_2")
        self.numLine = QtWidgets.QLineEdit(self.centralwidget)
        self.numLine.setGeometry(QtCore.QRect(320, 450, 91, 41))
        self.numLine.setStyleSheet("font: 11pt \"微软雅黑\";")
        self.numLine.setText("")
        self.numLine.setObjectName("numLine")
        self.endBtn = QtWidgets.QPushButton(self.centralwidget)
        self.endBtn.setGeometry(QtCore.QRect(490, 460, 161, 51))
        self.endBtn.setStyleSheet("background-color: rgb(255, 0, 0);\n"
"font: 75 14pt \"微软雅黑\";")
        self.endBtn.setObjectName("endBtn")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 692, 23))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.beginBtn.setToolTip(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:12pt; font-weight:600;\">请确定id和cookie输入无误再开始爬取</span></p></body></html>"))
        self.beginBtn.setText(_translate("MainWindow", "3. 开始爬取"))
        self.label.setText(_translate("MainWindow", "爬取结果"))
        self.cookieLine.setToolTip(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:12pt; font-weight:600;\">请更新cookie，不填则使用上次cookie</span></p></body></html>"))
        self.cookieLabel.setText(_translate("MainWindow", "1. 输入浏览器Cookie："))
        self.cookieLabel_2.setText(_translate("MainWindow", "2. 输入起始数字："))
        self.numLine.setToolTip(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:12pt; font-weight:600;\">请更新cookie，不填则使用上次cookie</span></p></body></html>"))
        self.endBtn.setToolTip(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:12pt; font-weight:600;\">请确定id和cookie输入无误再开始爬取</span></p></body></html>"))
        self.endBtn.setText(_translate("MainWindow", "中断爬虫"))

