#coding:utf-8
import urllib
import re
import selenium;
from selenium import webdriver

def getPageContent(url):
    page = urllib.urlopen(url)
    return page.code,page.read();


def parseAurl(html):
    reg = '"(/.+?\.jpg)"'
    reg_img = re.compile(reg)
    return reg_img.findall(html)

def scan(url):
    code,html = getPageContent(url);
    print str(code)+"==========="+html;
    if code==200 :
        list = parseAurl(html)
        for image in list:
            print image;



driver = webdriver.Chrome()
driver.get("http://www.baidu.com/")
print driver.get_network_conditions()
# scan("http://www.jd.com/")
