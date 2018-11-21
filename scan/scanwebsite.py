# coding:GBK

# 网站扫描工具，扫描网站内部中所有的url，js等资源
# author:wuwh
import Queue
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import urllib
import urlparse
# import LogFile
# import logfile
from logfile import *
from webmap import *


class ScanWebSite(object):


    def __init__(self,scanUrl,logname="scan.log",deep=2,domain="10086"):
        self.domain=domain
        # 已经扫描的地址
        self.listhassacnaurl=[]
        self.htmllist=Queue.Queue()
        self.basedoamin=""
        self.scanurl = scanUrl
        self.logFile = LogFile(fileName=logname)
        map = WebsitrTree(startValue=scanUrl)
        self.webtree = map
        self.deep=deep
    def start(self):
        self.chrome = webdriver.Chrome()

        self.chrome.set_window_size(0, 0)
        if self.scanurl != None:
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
                    print "开始扫描：" + html
                    print self.basedoamin
                    print "#################################################################################"

                    # 相同域名下
                    if str(html).find(self.basedoamin) > -1:
                        self.execute(html)
                    else:
                        print "要扫描的:"+str(html)+" 不是本站点下的url不进行扫描"
                    # 放入已经扫描队列中
                    self.listhassacnaurl.append(html)
                except Exception as e:
                    print e
                    pass
                print "当前扫描队列长度为 ："+str(self.htmllist.qsize())
            else:
                print str(html)+" 已经扫描过，不用再扫描"

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
            print "不是同一个域名下的，不扫描"
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
            goodssrc = ele.get_attribute("goodsurl")
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
                    print ""+childrenurl+" 是第"+str(deep)+"层  ,配置扫面层级为： "+str(self.deep)
                    if deep <= self.deep:
                       print '将'+ childrenurl+" 添加到扫描队列中，当前扫描队列为: "+str(self.htmllist.qsize() )
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
            self.logFile.writeLine(visiturl+"    "+str(code))

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
    scanobj = ScanWebSite(scanUrl="http://wap.sn.10086.cn/h5/index/html/home.html")
    scanobj.start()
