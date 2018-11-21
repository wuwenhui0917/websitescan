#coding=GBK
import urllib
from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
import threading
import Queue
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import urllib
import urlparse


from multiprocessing import Process


class WebsitrTree(object):
    def __init__(self,startValue):
        startNode=TreeNode(nodevalue=startValue,parentnode=None)
        self.startnode = startNode
    def addChild(self,childValue,paraentValue):
        startnode = self.startnode
        startnode.addChild(childValue,parentValue=paraentValue)

    def getDeep(self,nodeValue):
        # i=0;
        startNode = self.startnode
        # if startNode.value==nodeValue:
        #     return 0
        node = startNode.findNodeValue(nodevalue=nodeValue)
        if node!=None:
            return node.level
        return -1


#
# 树形节点
# author:wuwh
class TreeNode(object):
    def __init__(self,nodevalue,parentnode=None):
        #本节点上的数据
        self.value=nodevalue
        #此节点的子节点
        self.children = []
        if parentnode==None:
            self.level=0;
        else :
            self.level=parentnode.level+1
        self.parent=parentnode
    def addChildValue(self,childvalue):
        child =TreeNode(nodevalue=childvalue,parentnode=self)
        self.children.append(child)
    def addChild(self,chaildVlaue,parentValue):
        if self.value == parentValue:
            self.addChildValue(chaildVlaue)
            return
        for child in self.children:
            child.addChild(chaildVlaue,parentValue)
    def findNodeValue(self,nodevalue):
        if self.value ==nodevalue:
            return self
        for children in self.children:
            findNode =  children.findNodeValue(nodevalue)
            if findNode!=None:
                return findNode
        return None


    def printNode(self):
        # print "     "+self.value+"     "
        print self.value+" : children ------->[   "

        for node in self.children:
            node.printNode()
        print "  ]"





class LogFile(object):

    def __init__(self,fileDir="./",fileName=None):
        self.fileDir=fileDir
        self.fileName=fileName
        try:
            self.openfile =open(str(fileDir)+str(fileName),"a+")
        except Exception as e :
            print "文件打开异常"

    def writeLine(self,line):
        if self.openfile!=None:
            self.openfile.writelines(line+"\n")

    def close(self):
        if self.openfile:
            self.openfile.close()


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
            # print p
            thexecute = handleThread(query[1],self)
            thexecute.start()
            # self.send_response(200)
            # self.send_header('Content-type', 'text/html')
            # self.end_headers()
            # self.wfile.write("ok====="+query[1])
        else:
            self.wfile.write("hello===="+path)

class ScanWebSite(object):


    def __init__(self,domain="10086.cn.log",scanUrl=None):
        self.domain=domain
        # 已经扫描的地址
        self.listhassacnaurl=[]
        self.htmllist=Queue.Queue()
        self.basedoamin=""
        self.scanurl = scanUrl
        self.logFile = LogFile(fileName=domain)
        map = WebsitrTree(startValue=scanUrl)
        self.webtree = map
        self.deep=2
    def start(self):
        self.chrome = webdriver.Chrome()

        self.chrome.set_window_size(0, 0)
        if self.scanurl !=None:
            self._startURL(self.scanurl)

    def _close(self):
        self.chrome.close()
        self.logFile.close()

    def _startURL(self,url):
        urlinfos = urlparse.urlparse(url)
        self.basedoamin = urlinfos.netloc
        self.htmllist.put(url)
        while not self.htmllist.empty():
            html = self.htmllist.get()
            if html not in self.listhassacnaurl:
                try:
                    print "#################################################################################"
                    print "开始扫描" + html
                    print self.basedoamin
                    print "#################################################################################"

                    # 相同域名下
                    if str(html).find(self.basedoamin) > -1:
                        self.execute(html)
                    else:
                        print "不符合要求"
                    # 放入已经扫描队列中
                    self.listhassacnaurl.append(html)
                except Exception as e:
                    print e
                    pass
                print "任务队列长度为："+str(self.htmllist.qsize())
        self._close()

    def getRealUrl(self, url, currenturl):
        strurl = str(url)
        # if(strUrl.startswith("./")):
        #     return currentUrl+strUrl;
        # if(strUrl.startswith("..")):
        #     strUrl.split("")
        if strurl.startswith("http"):
            return strurl
        else:
            return urlparse.urljoin(currenturl, url)
            # if strUrl.startswith("/") or strUrl.startswith("."):
            #     return urlparse.urljoin(currentUrl,url);

            # return None


    def execute(self,baseurl):
        # chrome.get("http://service.sn.10086.cn/pch5/index/html/index.html")
        self.chrome.get(baseurl)
        time.sleep(1)
        # 设置
        # parseUrl(baseurl)
        urlinfos = urlparse.urlparse(str(baseurl))
        if self.basedoamin != urlinfos.netloc:
            # print basedoamin + "============" + urlinfos.netloc
            print "domain 不一致"
            return
        # strpasswprd = raw_input("登陆成功后请按任意键: ");
        # print "Received input is : ", str
        # 处理url获取domain等信息
        # parseUrl(baseurl)
        listurl = []
        list = self.chrome.find_elements(By.TAG_NAME, "a")
        print "a========="+str(len(list))
        for ele in list:
            url = ele.get_attribute("href")
            goodssrc = ele.get_attribute("goodsurl");
            # print url;
            strUrl = str(url)
            print strUrl
            # if not str(url).startswith("http") and str(url)!='' and url !=None :
            #     listurl.append(url)
            # if strUrl.startswith("http") :
            #     listurl.append(url)
            # if strUrl.startswith("/"):
            #     listurl(domain+strUrl);
            if not strUrl.startswith("java") and url != None and strUrl != '':
                childrenurl = self.getRealUrl(strUrl, baseurl)
                listurl.append(childrenurl)
                if childrenurl not in self.listhassacnaurl:
                    #加入网站地图中
                    self.webtree.addChild(childValue=childrenurl,paraentValue=baseurl)
                    deep = self.webtree.getDeep(childrenurl)
                    print ""+childrenurl+" 是第"+str(deep)+"层 扫描最大层为"+str(self.deep)
                    if deep <= self.deep:
                       print '将'+ childrenurl+"加入后续扫描队列 扫描队列长度为:"+str(self.htmllist.qsize() )
                       self.htmllist.put(childrenurl)
                    # print "扫描队列长度为：" + str(len(self.htmllist))

            if goodssrc != None and goodssrc != '':
                listurl.append(self.getRealUrl(goodssrc, baseurl))
                if self.getRealUrl(goodssrc, baseurl) not in self.listhassacnaurl:
                    self.htmllist.put(self.getRealUrl(goodssrc, baseurl))

                # print 'goodsurl::::::::::::::' + goodssrc

        # 处理图片
        imagess = self.chrome.find_elements(By.TAG_NAME, "img")
        for img in imagess:
            imgsrcurl = img.get_attribute("src")
            strImgsrc = str(imgsrcurl)
            if strImgsrc != None and strImgsrc != '':
                # print 'img:url' + strImgsrc
                listurl.append(self.getRealUrl(strImgsrc, baseurl))

        # css 扫描
        links = self.chrome.find_elements(By.TAG_NAME, "link")
        for link in links:
            linksrcurl = link.get_attribute("href")
            strlinksrcurl = str(linksrcurl)
            if strlinksrcurl != None and strlinksrcurl != '':
                # print 'link:url' + strlinksrcurl
                listurl.append(self.getRealUrl(strlinksrcurl, baseurl))
        # 扫面js
        scriptlinks = self.chrome.find_elements(By.TAG_NAME, "script")
        for jslink in scriptlinks:
            linksrcurl = jslink.get_attribute("src")
            strjssrcurl = str(linksrcurl)
            if strjssrcurl != None and strjssrcurl != '':
                # print 'script:url' + strjssrcurl
                listurl.append(self.getRealUrl(strjssrcurl, baseurl))

        # imglist  = chrome.find_elements(By.TAG_NAME,"a")
        # chrome.close();

        for visiturl in listurl:
            code = self.getPageContent(visiturl)
            self.logFile.writeLine(visiturl+"="+str(code))

            # print str(visiturl) + "\t=============result========:" + str(code)
    #
    # 获取页面响应码
    #
    def getPageContent(self,url):
        try:
            page = urllib.urlopen(url)
            if page.code != 200:
                print url + "\t" + str(page.code)
            return page.code;
        except IOError as e:
            print "errorurl==============================" + str(url)
            return -1

if __name__ == '__main__':
    print '启动http服务'
    httpserver=HTTPServer(("127.0.0.1",9999),handleClass);
    httpserver.serve_forever();

