import socket
from src.utils import *

s = socket.socket()
s.connect(("127.0.0.1", 8080))  # 客户端向服务端发起连接
data = {
    "cmd": "login",
    "user": "wangtao",
    "pwd": "111"
}
send(s, data)
s.close()
