from PyQt5 import QtWidgets
from . import main_window

"""
实现各种界面窗口的直接继承
"""


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.new = main_window.Ui_MainWindow()
        self.new.setupUi(self)
        self.new.retranslateUi(self)


