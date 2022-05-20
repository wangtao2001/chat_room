import hashlib
import sys
import socket
import time

from PyQt5.QtWidgets import QApplication, QMessageBox
from src.ui.windows import *
from src.utils import *

conn: socket.socket
server_ip = "127.0.0.1"  # 后期显式指定(包含测试连接..)
server_port = "8080"
dialog_window: MainWindow  # 将窗口提升为module变量的位置，否则对象会在login_window关闭后销毁
# 不继续使用mian_window是因为会与windows.py中的main_window重复
# 而login_window作为__main__中定义的变量不需要声明即可在函数中使用
# 同样，对这些变量(全局变量)的使用不需要global声明， 只有赋值才需要
current_session = ""  # 当前会话(是聊天室还是私聊, 默认是聊天室)
username: str  # 当前用户名


# 断开连接 发送断开信息
def close_socket():
    send(conn, {'cmd': 'close'})
    conn.shutdown(2)
    conn.close()


# 登录
def on_login_clicked():
    global conn, dialog_window, username
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
        if server_response['response'] == 'fail':  # 登陆失败
            close_socket()
            QMessageBox.warning(login_window, "警告", "账号或密码错误或用户未注册", QMessageBox.Yes | QMessageBox.No)
        else:
            dialog_window = MainWindow()
            # 以下是对dialog_window的配置 与__main__中的步骤相同
            dialog_window.closeEvent = lambda e: close_socket()
            dialog_window.new.title.setText(f"欢迎：{username}")
            # 为发送消息与发送文件按钮绑定功能
            dialog_window.new.sendButton.clicked.connect(on_send_clicked)
            dialog_window.new.sendFileButton.clicked.connect(on_send_file_clicked)
            dialog_window.show()
            login_window.close()


# 注册
def on_register_clicked():
    global conn, username
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
        if server_response['response'] == 'ok':
            close_socket()
            QMessageBox.information(login_window, "消息", "注册成功", QMessageBox.Yes | QMessageBox.No)
        elif server_response['response'] == 'fail':
            close_socket()
            QMessageBox.warning(login_window, "警告", "注册失败", QMessageBox.Yes | QMessageBox.No)


# 发送消息
def on_send_clicked():
    message = dialog_window.new.messageEdit.text()
    if message == "":
        QMessageBox.warning(dialog_window, "警告", "发送消息不能为空", QMessageBox.Yes | QMessageBox.No)
    else:
        send(conn, {'cmd': 'chat', 'peer': current_session, 'msg': message})
        # 往窗口上添加一条记录
        dialog_window.history.append([username, time.strftime('%Y/%m/%d %H:%M', time.localtime(time.time())), message])
        dialog_window.flush_history()  # 更新聊天记录


# 发送文件
def on_send_file_clicked():
    print("发送文件")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    login_window = LoginWindow()
    login_window.new.loginButton.clicked.connect(on_login_clicked)  # 分别绑定槽函数
    login_window.new.registerButton.clicked.connect(on_register_clicked)
    login_window.show()
    sys.exit(app.exec_())
