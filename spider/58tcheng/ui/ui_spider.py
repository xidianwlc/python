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
        self.beginBtn.setGeometry(QtCore.QRect(20, 420, 161, 51))
        self.beginBtn.setStyleSheet("background-color: rgb(255, 85, 0);\n"
"font: 75 14pt \"微软雅黑\";")
        self.beginBtn.setObjectName("beginBtn")
        self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit.setGeometry(QtCore.QRect(210, 40, 441, 461))
        self.textEdit.setStyleSheet("background-color: rgb(170, 170, 127);\n"
"font: 11pt \"微软雅黑\";\n"
"border-color: rgb(0, 0, 0);")
        self.textEdit.setObjectName("textEdit")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(210, 10, 61, 20))
        self.label.setStyleSheet("font: 75 11pt \"微软雅黑\";")
        self.label.setObjectName("label")
        self.cookieLine = QtWidgets.QLineEdit(self.centralwidget)
        self.cookieLine.setGeometry(QtCore.QRect(20, 220, 161, 41))
        self.cookieLine.setStyleSheet("font: 11pt \"微软雅黑\";")
        self.cookieLine.setText("")
        self.cookieLine.setObjectName("cookieLine")
        self.cookieLabel = QtWidgets.QLabel(self.centralwidget)
        self.cookieLabel.setGeometry(QtCore.QRect(20, 150, 151, 20))
        self.cookieLabel.setStyleSheet("font: 75 11pt \"微软雅黑\";")
        self.cookieLabel.setObjectName("cookieLabel")
        self.browserBtn = QtWidgets.QPushButton(self.centralwidget)
        self.browserBtn.setGeometry(QtCore.QRect(20, 310, 161, 51))
        self.browserBtn.setStyleSheet("background-color: rgb(255, 85, 0);\n"
"font: 12pt \"微软雅黑\";")
        self.browserBtn.setObjectName("browserBtn")
        self.comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox.setGeometry(QtCore.QRect(20, 50, 161, 41))
        self.comboBox.setObjectName("comboBox")
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
        self.beginBtn.setToolTip(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:12pt; font-weight:600;\">请确定cookie输入无误及PhantomJS启动成功再开始爬取</span></p></body></html>"))
        self.beginBtn.setText(_translate("MainWindow", "4. 开始爬取"))
        self.label.setText(_translate("MainWindow", "爬取结果"))
        self.cookieLine.setToolTip(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:12pt; font-weight:600;\">请更新cookie，不填则使用上次cookie</span></p></body></html>"))
        self.cookieLabel.setText(_translate("MainWindow", "2. 输入浏览器Cookie："))
        self.browserBtn.setToolTip(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:12pt; font-weight:600;\">启动PhantomJS无界面浏览器线程</span></p></body></html>"))
        self.browserBtn.setText(_translate("MainWindow", "3. 启动PhantomJS"))
        self.comboBox.setToolTip(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:14pt; font-weight:600;\">收到的简历还是回收站？</span></p></body></html>"))

