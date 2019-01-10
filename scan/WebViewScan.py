# coding:utf-8

# 网站扫描工具，扫描网站内部中所有的url，js等资源
# author:wuwh 测试使用
import time
import urllib2
import re

from selenium import webdriver
from selenium.webdriver.common.by import By
import urllib
import urlparse

chrome =None;
# chrome.set_window_size(0, 0)
# 当前domain
domain = '';
# 已经扫描列表
listhassacnaurl = []
# 需要扫描的html列表
htmllist = []
# 基本domain
basedoamin = 'service.sn.10086.cn'


def hasScan(url):
    return url in list


def close():
    chrome.close()


def parseUrl(str_url):
    urlinfos = urlparse.urlparse(str_url)
    domain = urlinfos.netloc
    return urlinfos;


def getPageContent(url):
    try:
        page = urllib2.urlopen(url)
        if page.code != 200:
            print url + "\t" + str(page.code)
        return page.code;
    except IOError as e:
        print "errorurl==============================" + str(url)
        return -1


def getRealUrl(url, currentUrl):
    strUrl = str(url)
    # if(strUrl.startswith("./")):
    #     return currentUrl+strUrl;
    # if(strUrl.startswith("..")):
    #     strUrl.split("")
    if strUrl.startswith("http"):
        return strUrl
    else:
        return urlparse.urljoin(currentUrl, url);
        # if strUrl.startswith("/") or strUrl.startswith("."):
        #     return urlparse.urljoin(currentUrl,url);

        # return None


def getImageInfo(listurl, chrome):
    list = chrome.find_elements(By.TAG_NAME, "img")


def startURL(url):
    urlinfos = urlparse.urlparse(url)
    basedoamin = urlinfos.netloc
    htmllist.append(url)
    for html in htmllist:
        if html not in listhassacnaurl:
            print "#################################################################################"
            print "开始扫描" + html
            print "#################################################################################"

            # 相同域名下
            if str(html).find(basedoamin) > -1:
                execute(html)
            # 放入已经扫描队列中
            listhassacnaurl.append(html)

    close()

##
## 获取页面内容
##
def getFileContent(url):
    try:
      page = urllib2.urlopen(url, timeout=3).read()
      return page;
    except Exception as e:
      print "context get error"
      return None



def execute(baseurl):
    # chrome.get("http://service.sn.10086.cn/pch5/index/html/index.html")
    chrome.get(baseurl)
    time.sleep(1)
    # 设置
    # parseUrl(baseurl)
    urlinfos = urlparse.urlparse(str(baseurl))
    if basedoamin != urlinfos.netloc:
        print basedoamin + "============" + urlinfos.netloc
        print "domain 不一致"
        return
    # strpasswprd = raw_input("登陆成功后请按任意键: ");
    # print "Received input is : ", str
    # 处理url获取domain等信息
    # parseUrl(baseurl)
    listurl = []
    list = chrome.find_elements(By.TAG_NAME, "a")
    for ele in list:
        url = ele.get_attribute("href")
        goodssrc = ele.get_attribute("goodsurl");
        print url;
        strUrl = str(url)
        # if not str(url).startswith("http") and str(url)!='' and url !=None :
        #     listurl.append(url)
        # if strUrl.startswith("http") :
        #     listurl.append(url)
        # if strUrl.startswith("/"):
        #     listurl(domain+strUrl);
        if not strUrl.startswith("java") and url != None and strUrl != '':
            listurl.append(getRealUrl(strUrl, baseurl))
            if getRealUrl(strUrl, baseurl) not in listhassacnaurl:
                htmllist.append(getRealUrl(strUrl, baseurl))

        if goodssrc != None and goodssrc != '':
            listurl.append(getRealUrl(goodssrc, baseurl))
            if getRealUrl(goodssrc, baseurl) not in listhassacnaurl:
                htmllist.append(getRealUrl(goodssrc, baseurl))

            print 'goodsurl::::::::::::::' + goodssrc

    # 处理图片
    imagess = chrome.find_elements(By.TAG_NAME, "img")
    for img in imagess:
        imgsrcurl = img.get_attribute("src")
        strImgsrc = str(imgsrcurl)
        if strImgsrc != None and strImgsrc != '':
            print 'img:url' + strImgsrc
            listurl.append(getRealUrl(strImgsrc, baseurl))

    # css 扫描
    links = chrome.find_elements(By.TAG_NAME, "link")
    for link in links:
        linksrcurl = link.get_attribute("href")
        strlinksrcurl = str(linksrcurl)
        if strlinksrcurl != None and strlinksrcurl != '':
            print 'link:url' + strlinksrcurl
            cssrealurl = getRealUrl(strlinksrcurl, baseurl)
            listurl.append(cssrealurl)
            csscontent = getPageContent(cssrealurl)
            try:
                #提取css中的url：
                cssurl = re.findall(r"background:url\((.*)\)", csscontent, re.S)
                for csseleurl in cssurl:

                    cssrealurl = getRealUrl(csseleurl, cssrealurl)
                    print "提取出url为："+str(cssrealurl)
                    listurl.append(cssrealurl)
            except Exception as e:
                print "提取css 中的url异常"

    # 扫面js
    scriptlinks = chrome.find_elements(By.TAG_NAME, "script")
    for jslink in scriptlinks:
        linksrcurl = jslink.get_attribute("src")
        strjssrcurl = str(linksrcurl)
        if strjssrcurl != None and strjssrcurl != '':
            print 'script:url' + strjssrcurl
            listurl.append(getRealUrl(strjssrcurl, baseurl))

    # imglist  = chrome.find_elements(By.TAG_NAME,"a")
    # chrome.close();

    try:
        #处理html 里面的load等方法
        pageinfo = getPageContent(baseurl)
        loadinfo =re.findall(r"load\('(.*)'\)", pageinfo, re.S)
        print '提取 html 中 load加载url'
        for loadtext in loadinfo:
            print "提取出来的地址为："+str(loadtext)
            reailurl = getRealUrl(loadtext, baseurl)
            print "转化成访问地址为：" + str(reailurl)
            listurl.append(reailurl)
    except Exception as e:
          print '提取html 内容异常'




    for visiturl in listurl:
        code = getPageContent(visiturl)
        print str(visiturl) + "\t=============result========:" + str(code)


if __name__ == '__main__':
    # strurl = raw_input("请输入要扫描的页面: ")
    # if strurl!=None and strurl!='':
        # execute("http://service.sn.10086.cn/pch5/index/html/index.html")
        # execute(strurl)
        # pageinfo = getFileContent("http://www.ln.10086.cn/service/static/zhaopin/testDL.html")
        # pageinfo="load("http://wwww.hello.com")"
        # brand = re.findall(r"load\('(.*)'\)", pageinfo, re.S)[0]
        # urlcontext = " background:url(../images/close.png); float:left; margin:12px 0 0 20px;cursor:pointer;}"
        urlcontext = getFileContent("http://www.ln.10086.cn/service/static/style/common/ln_index.css")
        print urlcontext
        cssurl = re.findall(r"url\((.+?)\)", urlcontext)
        for csseleurl in cssurl:
            print csseleurl

            print "提取出url为：" + str(csseleurl)

        print cssurl



    # url=("http://www.baidu.com/a/c/d",None);
    #
    # print getRealUrl(url[1],url[0])

    # chrome.execute_script('alert(\'dddd\')')
