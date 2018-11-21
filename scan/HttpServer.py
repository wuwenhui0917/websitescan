# coding:GBK
from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
import threading
from configfile import *
from multiprocessing import Process
from scanwebsite import *


class myprocess(Process):

    def __init__(self, group=None, target=None, name=None, args=(), kwargs={}):
        super(myprocess, self).__init__(group, target, name, args, kwargs)

    def run(self):
        scanobj = ScanWebSite(scanUrl="http://wap.sn.10086.cn/h5/index/html/home.html")
        scanobj.start()



class handleThread(threading.Thread):
    def __init__(self, jsonParam,handleClass ):
        super(handleThread, self).__init__()#注意：一定要显式的调用父类的初始化函数。
        self.param = jsonParam
        self.server = handleClass
        self.error = None
        print jsonParam
        print handleClass
        urlinfo = urlparse.urlparse(self.param)
        params = urlparse.parse_qs(urlinfo.query)
        if params.get("transid"):
            self.transid = params.get("transid")[0]
        else:
            self.error = "transid must not null"
        if params.get("scanurl"):
            self.scanurl = urllib.unquote(params.get("scanurl")[0])
        else:
            self.error = "scanurl must not null"
        if params.get("deep"):
            self.deep = params.get("deep")[0]
        else:
            self.deep = 1

    def checkparam(self):
        return self.error

    def run(self):
        print self.getName()+"线程开始，扫描地址为："+str(self.scanurl)+" 扫描深度为："+str(self.deep)+" 扫描日志为："+str(self.transid)+".log"
        scanobj = ScanWebSite(scanUrl=self.scanurl, logname=str(self.transid)+".log")
        scanobj.start()

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
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        print 'dsdsds'
        path = self.path
        print 'path........'+path
        query = urllib.splitquery(path)
        print query[0]

        self._writeheads()
        if query[0].startswith('/scan'):
            thexecute = handleThread(path, self)
            checkinfo = thexecute.checkparam()
            if checkinfo:
                self.wfile.write(checkinfo)
                return
            self.wfile.write("ok")
            # p = myprocess()
            # p.start()
            thexecute.start()
            # self.send_response(200)
            # self.send_header('Content-type', 'text/html')
            # self.end_headers()
            # self.wfile.write("ok====="+query[1])
        else:
            self.wfile.write("hello===="+path)

if __name__ == '__main__':
    print '启动http'
    config = ConfigFile()
    ip = config.getvalue("bindip")
    port = config.getvalue("port")

    print "启动 http 服务 绑定ip为"+str(ip)+"绑定端口为："+str(port)
    HOST, PORT = str("127.0.0.1"), int(port)

    httpserver = HTTPServer((HOST,PORT), handleClass)
    httpserver.serve_forever()

