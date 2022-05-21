import re

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import QObject, pyqtSignal, QStringListModel
from PyQt5.QtWidgets import QApplication
from typing import List, Dict

from src.ui import main_window, login_window

"""
实现各种界面窗口的直接继承
"""


class LoginWindow(QtWidgets.QDialog):
    def __init__(self):
        super(LoginWindow, self).__init__()
        self.new = login_window.Ui_Dialog()
        self.new.setupUi(self)
        self.new.retranslateUi(self)


class MainWindow(QtWidgets.QMainWindow):
    history: List[list] = []
    users: Dict[str, bool] = {}  # 所有用户与用户被选择
    ulist: List[str] = []  # users中所有的用户转储对象，同时保证了渲染顺序与这里的顺序一样

    def __init__(self):
        super(MainWindow, self).__init__()
        self.new = main_window.Ui_MainWindow()
        self.new.setupUi(self)
        self.new.retranslateUi(self)

    # 刷新聊天记录
    # 考虑到这里的循环遍历比较耗时，故使用多线程来循环，完成后刷新页面，进程结束，下同
    def fresh_history(self):
        myname = re.split("：| <- ", self.new.title.text())[1]  # 有两种title
        fresh_thread = FreshHistoryThread(self.history, myname)
        fresh_thread.finishSignal.connect(self.fresh_history_callback)
        fresh_thread.run()

    def fresh_history_callback(self, content):
        self.new.messageDialog.setHtml(QtCore.QCoreApplication.translate("MainWindow", content))
        # 以下保持视图始终在dialog底部
        self.new.messageDialog.ensureCursorVisible()  # 游标可用
        cursor = self.new.messageDialog.textCursor()  # 设置游标
        pos = len(self.new.messageDialog.toPlainText())  # 获取文本尾部的位置
        cursor.setPosition(pos)  # 游标位置设置为尾部
        self.new.messageDialog.setTextCursor(cursor)  # 滚动到游标位置
        self.new.messageEdit.setText("")  # 按照设计原则这两句放在这比较好
        QApplication.processEvents()

    # 刷新用户列表，这里就不用多线程了
    def fresh_user_list(self):
        slm = QStringListModel()  # 数据模型
        self.ulist = []  # 每次刷新都与self.user同步，只是一个转储对象
        for user in self.users.keys():
            name = '世界聊天室' if user == '' else user
            if self.users[user]:
                name += ' (*)'
            self.ulist.append(name)
        slm.setStringList(self.ulist)
        self.new.userList.setModel(slm)  # 将QListView与模型绑定
        # 接下来是选定用户的操作


# 使用多线程处理页刷新问题
class FreshHistoryThread(QObject):
    finishSignal = pyqtSignal(str)

    def __init__(self, history: list, myname: str):
        super().__init__()
        self.history = history
        self.name = myname

    # 处理业务逻辑
    def run(self):
        # 这里加一个小逻辑，如果是自己的名字，就标注，其他的不标
        # 后期甚至可以写样式
        # 自己的名字可以用title获取
        content = "<!DOCTYPE HTML><html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n p, li { white-space: pre-wrap; }\n""</style></head><body style=\" font-family:\'SimSun\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
        for m in self.history:
            content += f"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:11pt;\">{m[1]}</span></p>\n"
            if m[0] == self.name:
                content += f"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:11pt; color: green; font-weight: 700; \">我: {m[2]}</span></p>\n"
            else:
                content += f"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:11pt;\">{m[0]}: {m[2]}</span></p>\n"
            content += "<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:11pt;\"><br /></p>\n"
        content += "</body></html>"
        self.finishSignal.emit(content)
