# coding:GBK
from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
import threading
from configfile import *
from multiprocessing import Process
from scanwebsite import *
from SftpClient import *
from httpclient import *

config = ConfigFile()


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
        scanobj = ScanWebSite(scanUrl=self.scanurl, deep=int(self.deep), logname=str(self.transid)+".log")
        scanobj.start()
        ftptag = int(config.getvalue("ftptag"))
        if ftptag == 1:
            print "frpip="+config.getStringvalue("ftpip")
            print "ftppwd="+config.getStringvalue("ftppwd")
            print "ftpuser="+config.getStringvalue("ftpuser")
            sft = FtpClient(ftpip=config.getStringvalue("ftpip"),
                            ftppasswd=config.getStringvalue("ftppwd"),
                            ftpuser=config.getStringvalue("ftpuser")
                            )
            try:
                sft.connection()
                sft.upload(str(self.transid)+".log",config.getStringvalue("ftpdir")+"/"+str(self.transid)+".log")
                print(str(self.transid)+" 文件上传成功上传成功")
                httpurl = config.getvalue("ftpcallback")
                if httpurl:
                    httpclient = HttpClient(str(httpurl))
                    _params = {"transid": self.transid, "logfile": str(self.transid)+".log"}

                    if httpclient.do_get(_params):
                        print("回调："+self.transid+"成功")
            except Exception as e:
                print("[ERROR:] 链接异常", e)
            finally:
                if sft:
                    sft.close()


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
    print '启动服务端'

    ip = str(config.getvalue("bindip")).strip()
    port = config.getvalue("port")
    # ip = "127.0.0.1"

    print "启动 http 服务 绑定ip为"+ip+"绑定端口为："+str(port)
    HOST, PORT = ip, int(port)
    httpserver = HTTPServer((HOST, PORT), handleClass)
    httpserver.serve_forever()

