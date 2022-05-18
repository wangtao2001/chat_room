#### <img alt="" src="./assets/readme-icon-introduction.png" style="display: inline-block;" width=3%/>介绍

使用socketserver搭建的聊天室

特性：
 - 客户端与服务端分离
 - 支持用户的登录与注册
 - 精美的UI (基于PyQt5)
 - 支持世界聊天室与私聊
 - 保存聊天记录
 - 传输数据加密 (基于AES)

可能会支持：
 - 服务器显式配置
 - 服务端数据库的使用
 - 后台管理

#### <img alt="" src="./assets/readme-icon-framework.png" style="display: inline-block;" width=3%/> 软件架构

#### <img alt="" src="./assets/readme-icon-compile.png" style="display: inline-block;" width=3%/>运行

首先运行服务端
```shell
$ python3 server.py
```

然后运行客户端
```shell
$ python3 client.py
```

如使用pyinstaller等工具时，请将server.py目录与client.py目录分开打包
