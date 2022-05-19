import hashlib

from PyQt5.QtWidgets import QApplication, QMessageBox
from src.ui.windows import *
from src.utils import *

import sys
import socket

conn: socket.socket
server_ip = "127.0.0.1"  # 后期显式指定(包含测试连接..)
server_port = "8080"


# 断开连接 发送断开信息
def close_socket():
    send(conn, {'cmd': 'close'})
    conn.shutdown(2)
    conn.close()


# 登录
def on_login_clicked():
    global conn
    conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # IPv4 TCP连接
    conn.settimeout(5)
    username, passwd = login_window.new.user.text(), login_window.new.pwd.text()
    if username == "" or passwd == "":  # 账号密码为空
        close_socket()  # 这里 QMessage会阻塞进程，所以关闭连接要放在前面
        QMessageBox.warning(login_window, "警告", "账号或密码不能为空", QMessageBox.Yes | QMessageBox.No)
    else:
        conn.connect((server_ip, int(server_port)))  # 连接额服务器
        send(conn, {'cmd': 'login', 'user': username,  # 发送登录信息
                    'pwd': hashlib.sha1(passwd.encode('utf-8')).hexdigest()})
        server_response = recv(conn)
        print(server_response)
        if server_response['response'] == 'fail':  # 登陆失败
            close_socket()
            QMessageBox.warning(login_window, "警告", "账号或密码错误或用户未注册", QMessageBox.Yes | QMessageBox.No)
        else:
            print("登陆成功")


# 注册
def on_register_clicked():
    global conn
    conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # IPv4 TCP连接
    conn.settimeout(5)
    username, passwd = login_window.new.user.text(), login_window.new.pwd.text()
    if username == "" or passwd == "":
        close_socket()
        QMessageBox.warning(login_window, "警告", "账号或密码不能为空", QMessageBox.Yes | QMessageBox.No)
    else:
        conn.connect((server_ip, int(server_port)))
        send(conn, {'cmd': 'register', 'user': username,  # 发送注册信息
                    'pwd': hashlib.sha1(passwd.encode('utf-8')).hexdigest()})
        server_response = recv(conn)
        print(server_response)
        if server_response['response'] == 'ok':
            close_socket()
            QMessageBox.information(login_window, "消息", "注册成功", QMessageBox.Yes | QMessageBox.No)
        elif server_response['response'] == 'fail':
            close_socket()
            QMessageBox.warning(login_window, "警告", "注册失败", QMessageBox.Yes | QMessageBox.No)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    login_window = LoginWindow()
    login_window.new.loginButton.clicked.connect(on_login_clicked)  # 分别绑定槽函数
    login_window.new.registerButton.clicked.connect(on_register_clicked)
    login_window.show()
    sys.exit(app.exec_())
