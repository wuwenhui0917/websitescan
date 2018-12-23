#coding=GBK
import threading
import urllib2
import urlparse


class ScanThread(threading.Thread):
    def __init__(self,LogFile,listurl,htmllist,basedomain,scansite):

        threading.Thread.__init__(self)
        self.logfile = LogFile
        self.data = listurl
        self.basedoamin = basedomain
        self.scansite = scansite
        self.scansite.addthread()


    def getPageContent(self, url):
        try:
            page = urllib2.urlopen(url, timeout=3)
            if page.code != 200:
                print url + "\t" + str(page.code)
            return page.code
        except IOError as e:
            print "errorurl==============================" + str(url)
            return -1

    def run(self):

        #print "扫描线程"+self.getName()+"开始...."


        if self.data:
            for visiturl in self.data:
                # print "thread................"+str(self.scansite.threadcount);
                code = self.getPageContent(visiturl)
                if self.logfile:

                    self.logfile.writeLine(str(visiturl).strip() + "    " + str(code))
                else:
                    print(str(visiturl).strip() + "    " + str(code))
                #加入已经扫描队列
                self.scansite.addHasUrl(visiturl)

                    # code = self.getPageContent(childrenurl)
                # if code == 200 :
                #     urlinfos = urlparse.urlparse(str(visiturl))
                #     if self.basedoamin == urlinfos.netloc:
                #         pagename = str(visiturl);
                #         if pagename.endswith("html") or pagename.endswith("jsp"):
                #
                #             print '将' + visiturl + " 添加到扫描队列中，当前扫描队列为: " + str(self.htmllist.qsize())
                #             self.htmllist.put(pagename)
                #         else:
                            #加入已经扫描的



                            # listurl.append(childrenurl)
                        # else :
                        #   self.logFile.writeLine(str(childrenurl).strip() + "    " + str(code))

        else :
            print "nodata"
        print "扫描："+self.getName()+" 结束"
        self.scansite.release();
