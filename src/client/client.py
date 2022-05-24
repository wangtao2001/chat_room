import hashlib
import os.path
import sys
import socket
import threading
import time

from PyQt5.QtCore import QDir
from PyQt5.QtWidgets import QMessageBox, QFileDialog
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
file_transfer_pending = False  # 文件等待传输


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
            # 绑定user_list选择功能
            dialog_window.new.userList.clicked.connect(on_session_select)
            # 尝试去获取当前的用户与历史聊天记录 这些消息会被子线程异步监听
            send(conn, {'cmd': 'get_users'})
            send(conn, {'cmd': 'get_history', 'peer': ''})
            # 创建一个子线程用以监听服务器消息，包括用于列表变更，聊天记录变更
            t = threading.Thread(target=recv_async, args=())
            t.setDaemon(True)  # 守护线程，主线程退出的时候子线程也退出
            t.start()
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


# 监听后台消息
def recv_async():
    global current_session
    while True:
        data = recv(conn)
        if data['type'] == 'get_users':  # 获取所有用户
            for user in [''] + data['data']:
                dialog_window.users[user] = False
            dialog_window.fresh_user_list()  # 刷新用户列表
        elif data['type'] == 'get_history':  # 主动获取聊天记录
            if data['peer'] == current_session:
                dialog_window.history = []
                for entry in data['data']:
                    dialog_window.history.append([entry[0], entry[1], entry[2]])
            dialog_window.fresh_history()
        elif data['type'] == 'broadcast':  # 聊天室有人发言
            if current_session == '':  # 当前就在聊天室
                dialog_window.history.append(
                    [data['peer'], time.strftime('%Y/%m/%d %H:%M', time.localtime(time.time())), data['msg']])
                dialog_window.fresh_history()
            else:
                dialog_window.users[""] = True  # 当前不在聊天室
                dialog_window.fresh_user_list()
        elif data['type'] == 'msg':  # 私聊
            if data['peer'] == current_session:  # 私聊对象与发送私聊消息的对象相同
                dialog_window.history.append(
                    [data['peer'], time.strftime('%Y/%m/%d %H:%M', time.localtime(time.time())), data['msg']])
                dialog_window.fresh_history()
            else:
                dialog_window.users[data['peer']] = True  # 不同
                dialog_window.fresh_user_list()
        elif data['type'] == 'peer_joined':
            dialog_window.users[data['peer']] = False  # 有人进入
            dialog_window.fresh_user_list()
        elif data['type'] == 'peer_left':  # 有人离开
            if data['peer'] in dialog_window.users.keys():
                del dialog_window.users[data['peer']]
            if data['peer'] == current_session:  # 当前私聊的人离开了，转换成聊天室
                current_session = ""
                dialog_window.users[""] = False
                dialog_window.new.title.setText(f"欢迎：{username}")
                dialog_window.new.sendFileButton.setEnabled(False)
                send(conn, {'cmd': 'get_history', 'peer': ''})
            dialog_window.fresh_user_list()
        elif data['type'] == 'file_request':  # 有人想要发送文件
            # recv_async 是子线程，但qt中的gui都要在主线程，所以这里不能直接使用QMessageBox
            # QMessageBox.information(dialog_window, "消息", f"{data['peer']}想要给你发送文件：{data['filename']} (大小：{data['size']}) 是否接收?", QMessageBox.Yes | QMessageBox.No)
            pass


# 发送消息
def on_send_clicked():
    message = dialog_window.new.messageEdit.text()
    if message == "":
        QMessageBox.warning(dialog_window, "警告", "发送消息不能为空", QMessageBox.Yes | QMessageBox.No)
    else:
        send(conn, {'cmd': 'chat', 'peer': current_session, 'msg': message})
        # 往窗口上添加一条记录
        dialog_window.history.append([username, time.strftime('%Y/%m/%d %H:%M', time.localtime(time.time())), message])
        dialog_window.fresh_history()  # 更新聊天记录


# 发送文件
def on_send_file_clicked():
    global file_transfer_pending
    try:
        dialog = QFileDialog()  # 对话框对象
        dialog.setFileMode(QFileDialog.AnyFile)  # 设置打开文件类型 这里是所有文件
        dialog.setFilter(QDir.Files)
        if dialog.exec():  # 打开文件
            filenames = dialog.selectedFiles()[0]  # 返回被选择的文件（可以打开多个, 选择第一个）
            filename = os.path.basename(filenames)  # 文件名basename
            size = os.path.getsize(filenames)  # 文件大小（字节）
            count = 0
            while not 1 < size < 1024 and count < 6:
                size /= 1024
                count += 1
            size = str(format(size, '.2f')) + ['B', 'KB', 'MB', 'GB', 'TB', 'PB'][count]  # 给文件大小附上单位
            send(conn, {'cmd': 'file_request', 'peer': current_session, 'filename': filename, 'size': size})  # 发送请求
            dialog_window.new.sendFileButton.setText("等待中")
            dialog_window.new.sendFileButton.setEnabled(False)
            QApplication.processEvents()
            file_transfer_pending = True

    except FileNotFoundError:
        QMessageBox.warning(dialog_window, "警告", "文件不存在", QMessageBox.Yes | QMessageBox.No)


# 选择用户
def on_session_select(qModelIndex):
    global current_session
    u = dialog_window.ulist[qModelIndex.row()]
    changed = False
    if qModelIndex.row() != 0:  # 选择的不是世界聊天室
        if current_session != u.rstrip(' (*)'):
            changed = True
            current_session = u.rstrip(' (*)')
            if not file_transfer_pending:
                dialog_window.new.sendFileButton.setEnabled(True)  # 只有私聊可以发文件
            dialog_window.users[current_session] = False
            dialog_window.new.title.setText(f"{current_session} <- {username}")
    else:
        if current_session != "":
            changed = True
            current_session = ""
            dialog_window.users[''] = False
            dialog_window.new.title.setText(f"欢迎：{username}")
            dialog_window.new.sendFileButton.setEnabled(False)
    dialog_window.fresh_user_list()
    if changed:  # 如果对象变化了就获取聊天记录刷新页面
        send(conn, {'cmd': 'get_history', 'peer': current_session})


if __name__ == "__main__":
    app = QApplication(sys.argv)
    login_window = LoginWindow()
    login_window.new.loginButton.clicked.connect(on_login_clicked)  # 分别绑定槽函数
    login_window.new.registerButton.clicked.connect(on_register_clicked)
    login_window.show()
    sys.exit(app.exec_())
