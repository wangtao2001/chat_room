# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\wangtao\Desktop\main_window.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(915, 683)
        MainWindow.setMinimumSize(QtCore.QSize(915, 683))
        MainWindow.setMaximumSize(QtCore.QSize(915, 683))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.title = QtWidgets.QLabel(self.centralwidget)
        self.title.setGeometry(QtCore.QRect(90, 0, 411, 121))
        font = QtGui.QFont()
        font.setFamily("HarmonyOS Sans")
        font.setPointSize(14)
        self.title.setFont(font)
        self.title.setObjectName("title")
        self.message_dialog = QtWidgets.QTextBrowser(self.centralwidget)
        self.message_dialog.setGeometry(QtCore.QRect(90, 100, 461, 431))
        self.message_dialog.setObjectName("message_dialog")
        self.user_list = QtWidgets.QListView(self.centralwidget)
        self.user_list.setGeometry(QtCore.QRect(560, 100, 241, 431))
        self.user_list.setObjectName("user_list")
        self.message_edit = QtWidgets.QLineEdit(self.centralwidget)
        self.message_edit.setGeometry(QtCore.QRect(90, 540, 461, 31))
        self.message_edit.setObjectName("message_edit")
        self.send = QtWidgets.QPushButton(self.centralwidget)
        self.send.setGeometry(QtCore.QRect(560, 540, 121, 31))
        font = QtGui.QFont()
        font.setFamily("HarmonyOS Sans")
        font.setPointSize(12)
        self.send.setFont(font)
        self.send.setObjectName("send")
        self.send_file = QtWidgets.QPushButton(self.centralwidget)
        self.send_file.setGeometry(QtCore.QRect(690, 540, 111, 31))
        font = QtGui.QFont()
        font.setFamily("HarmonyOS Sans")
        font.setPointSize(12)
        self.send_file.setFont(font)
        self.send_file.setObjectName("send_file")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 915, 26))
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
        self.title.setText(_translate("MainWindow", "欢迎：晚安白日梦"))
        self.message_dialog.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'SimSun\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:11pt;\">2020-5-18 19:37</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:11pt;\">晚安白日梦：你好呀!!</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:11pt;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:11pt;\">2020-5-18 19:37</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:11pt;\">小熊软糖：你好~</span></p></body></html>"))
        self.send.setText(_translate("MainWindow", "发送消息"))
        self.send_file.setText(_translate("MainWindow", "发送文件"))
