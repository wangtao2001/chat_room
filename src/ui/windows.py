from PyQt5 import QtWidgets
from src.ui import main_window, login_window

"""
实现各种界面窗口的直接继承
"""


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.new = main_window.Ui_MainWindow()
        self.new.setupUi(self)
        self.new.retranslateUi(self)


class LoginWindow(QtWidgets.QDialog):
    def __init__(self):
        super(LoginWindow, self).__init__()
        self.new = login_window.Ui_Dialog()
        self.new.setupUi(self)
        self.new.retranslateUi(self)
