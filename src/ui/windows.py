from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5.QtWidgets import QApplication
from typing import List

from src.ui import main_window, login_window

"""
实现各种界面窗口的直接继承
"""


class MainWindow(QtWidgets.QMainWindow):
    history: List[list] = []

    def __init__(self):
        super(MainWindow, self).__init__()
        self.new = main_window.Ui_MainWindow()
        self.new.setupUi(self)
        self.new.retranslateUi(self)

    # 考虑到这里的循环遍历比较耗时，故使用多线程来循环，完成后刷新页面，进程结束
    def flush_history(self):
        flush_thread = FlushHistoryThread(self.history)
        flush_thread.finishSignal.connect(self.flush_history_callback)
        flush_thread.run()

    def flush_history_callback(self, content):
        self.new.messageDialog.setHtml(QtCore.QCoreApplication.translate("MainWindow", content))
        self.new.messageEdit.setText("")  # 按照设计原则这两句放在这比较好
        QApplication.processEvents()


class LoginWindow(QtWidgets.QDialog):
    def __init__(self):
        super(LoginWindow, self).__init__()
        self.new = login_window.Ui_Dialog()
        self.new.setupUi(self)
        self.new.retranslateUi(self)


# 使用多线程处理页刷新问题
class FlushHistoryThread(QObject):
    finishSignal = pyqtSignal(str)

    def __init__(self, history: list):
        super().__init__()
        self.history = history

    # 处理业务逻辑
    def run(self):
        content = "<!DOCTYPE HTML><html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n p, li { white-space: pre-wrap; }\n""</style></head><body style=\" font-family:\'SimSun\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
        for m in self.history:
            content += f"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:11pt;\">{m[1]}</span></p>\n"
            content += f"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:11pt;\">{m[0]}: {m[2]}</span></p>\n"
            content += "<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:11pt;\"><br /></p>\n"
        content += "</body></html>"
        self.finishSignal.emit(content)
