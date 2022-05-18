from src.server.users_manage import *
from src.server.chat_history import *
from src.utils import *

import socketserver


class Handler(socketserver.BaseRequestHandler):
    clients = {}  # 所有用户， 保存了所有的client即 "username": socket
    users = load_users()  # 所有用户信息 "username":"passwd"
    history = load_history()  # 历史聊天记录 "receive": {"sender", time, msg}

    def setup(self) -> None:  # 对每一个线程都是不同的
        self.user = ''  # 当前连接的用户
        self.file_peer = ''  # 发送文件的用户
        self.authed = False  # 用户是否认证

    def handle(self):
        while True:
            data = recv(self.request)  # 获取用户请求的信息，请求信息类型以data['cmd']表示

            if not self.authed:  # 用户未认证
                self.user = data['user']
                if data['cmd'] == 'login':  # 登录
                    print("login")
                    if validate(Handler.users, data['user'], data['pwd']):
                        send(self.request, {'response': 'ok'})
                        self.authed = True
                        for user in Handler.clients.keys():  # 将刚刚登录的用户广播出去
                            send(Handler.clients[user].request, {'type': 'peer_joined', 'peer': self.user})
                        Handler.clients[self.user] = self
                    else:
                        send(self.request, {'response': 'fail', 'reason': '账号或密码错误！'})

                elif data['cmd'] == 'register':  # 注册
                    print("register")
                    if register(Handler.users, data['user'], data['pwd']):
                        send(self.request, {'response': 'ok'})
                    else:
                        send(self.request, {'response': 'fail', 'reason': '账号已存在！'})

            else:
                if data['cmd'] == 'get_users':  # 获取所有用户(不包含当前用户)
                    users = []
                    for user in Handler.clients.keys():
                        if user != self.user:
                            users.append(user)
                    send(self.request, {'type': 'get_users', 'data': users})

                elif data['cmd'] == 'get_history':  # 获取历史聊天记录, 从任何一方出发都可以获取所有记录
                    send(self.request, {'type': 'get_history', 'peer': data['peer'],  # 另一方用户
                                        'data': get_history(Handler.history, self.user, data['peer'])})

                elif data['cmd'] == 'chat' and data['peer'] != '':  # 私聊
                    send(Handler.clients[data['peer']].request,  # 指向具体的用户
                         {'type': 'msg', 'peer': self.user, 'msg': data['msg']})
                    append_history(Handler.history, self.user, data['peer'], data['msg'])  # 添加一条记录

                elif data['cmd'] == 'chat' and data['peer'] == '':  # 聊天室聊天
                    for user in Handler.clients.keys():
                        if user != self.user:
                            send(Handler.clients[user].request,  # 广播聊天内容
                                 {'type': 'broadcast', 'peer': self.user, 'msg': data['msg']})
                    append_history(Handler.history, self.user, '', data['msg'])  # 这里添加聊天记时不许要指定接收方

                elif data['cmd'] == 'file_request':  # 请求发送数据
                    Handler.clients[data['peer']].file_peer = self.user
                    send(Handler.clients[data['peer']].request,
                         {'type': 'file_request', 'peer': self.user, 'filename': data['filename'],
                          'size': data['size'], 'md5': data['md5']})

                elif data['cmd'] == 'file_deny' and data['peer'] == self.file_peer:  # 拒绝文件
                    self.file_peer = ''
                    send(Handler.clients[data['peer']].request, {'type': 'file_deny', 'peer': self.user})

                elif data['cmd'] == 'file_accept' and data['peer'] == self.file_peer:  # 接收文件
                    self.file_peer = ''
                    send(Handler.clients[data['peer']].request,
                         {'type': 'file_accept', 'ip': self.client_address[0]})

                elif data['cmd'] == 'close':  # 退出
                    self.finish()

    def finish(self):
        if self.authed:
            self.authed = False
            if self.user in Handler.clients.keys():
                del Handler.clients[self.user]  # 从当前连接用户中删除
            for user in Handler.clients.keys():  # 广播所有用户
                send(Handler.clients[user].request, {'type': 'peer_left', 'peer': self.user})


if __name__ == '__main__':
    app = socketserver.ThreadingTCPServer(('127.0.0.1', 8080), Handler)  # 在本地创建一个多线程服务
    app.serve_forever()  # 开启服务

