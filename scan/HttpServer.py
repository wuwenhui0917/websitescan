#coding=utf-8
import urllib
from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
import threading
import time

from multiprocessing import Pool

from multiprocessing import Process
from scanwebsite import *


class myprocess(Process):

    def __init__(self, group=None, target=None, name=None, args=(), kwargs={}):
        super(myprocess, self).__init__(group, target, name, args, kwargs)



    def run(self):
        scanobj = ScanWebSite(scanUrl="http://wap.sn.10086.cn/h5/index/html/home.html");
        scanobj.start();



class handleThread(threading.Thread):
    def __init__(self, jsonParam,handleClass ):
        super(handleThread, self).__init__()#注意：一定要显式的调用父类的初始化函数。
        self.param = jsonParam
        self.server = handleClass
        print jsonParam
        print handleClass

    def run(self):
        time.sleep(1)
        print self.getName()
        scanobj = ScanWebSite(scanUrl="http://wap.sn.10086.cn/h5/index/html/home.html");
        scanobj.start();

        # print self.getName()
        # self.server.send_response(200)
        # self.server.send_header('Content-type', 'text/html')
        # self.server.end_headers()
        # self.server.end_headers()
        # self.send_response(200)

        # self.server.send_response(200,"hello")
        # self.server.finish()
        # self.server.wfile.write("hello====")


class handleClass(BaseHTTPRequestHandler):



    def _writeheads(self):
        print self.path
        print self.headers
        self.send_response(200);
        self.send_header('Content-type', 'text/html');
        self.end_headers()

    def do_GET(self):
        print 'dsdsds'

        path = self.path
        print 'path........'+path;
        query = urllib.splitquery(path)
        print query[0]

        self._writeheads()


        if query[0].startswith('/scan'):
            self.wfile.write("ok");
            # p = myprocess()
            # p.start()
            thexecute = handleThread(query[1],self)
            thexecute.start()
            # self.send_response(200)
            # self.send_header('Content-type', 'text/html')
            # self.end_headers()
            # self.wfile.write("ok====="+query[1])
        else:
            self.wfile.write("hello===="+path)

if __name__ == '__main__':
    print '启动http服务成功成功'
    httpserver=HTTPServer(("127.0.0.1",9999),handleClass);
    httpserver.serve_forever();

