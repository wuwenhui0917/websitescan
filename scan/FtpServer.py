# coding:GBK

import os

from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer


def main():
    # 实例化用户授权管理
    authorizer = DummyAuthorizer()
    authorizer.add_user('user', '12345', 'C://', perm='elradfmwMT')  # 添加用户 参数:username,password,允许的路径,权限
    authorizer.add_anonymous(os.getcwd())  # 这里是允许匿名用户,如果不允许删掉此行即可

    # 实例化FTPHandler
    handler = FTPHandler
    handler.authorizer = authorizer

    # 设定一个客户端链接时的标语
    handler.banner = "welcome I.am wwh."

    handler.masquerade_address = '151.25.42.11'#指定伪装ip地址
    handler.passive_ports = range(60000, 65535)#指定允许的端口范围

    address = ("127.0.0.1", 21)  # FTP一般使用21,20端口
    server = FTPServer(address, handler)  # FTP服务器实例

    # set a limit for connections
    server.max_cons = 256
    server.max_cons_per_ip = 5

    # 开启服务器
    server.serve_forever()


if __name__ == '__main__':
    main()
