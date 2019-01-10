# coding:GBK
import os
from ftplib import FTP


class FtpClient(object):
    def __init__(self,host,user,passwd,timeout,port=21):
        self.host = host
        self.user=user
        self.passwd = passwd
        self.port = port
        self.timeout = timeout
        self.ftp = FTP()

    def connection(self):
        try:
            self.ftp.connect(self.host,int(self.port),int(self.timeout))
            self.ftp.login(self.user,self.passwd)
            print self.ftp.getwelcome()
        except Exception as e:
            print ("ftp Error:", e)
            if self.ftp:
                self.ftp.close()

    def upload(self,localfile, remotedir):
        filename = os.path.basename(localfile)
        print filename
        print remotedir
        # remotetempdir = remotedir
        # if str(remotedir).endswith("/"):
        #     remotetempdir = remotetempdir + filename
        # self.ftp.cwd(remotedir)
        self.ftp.storbinary('STOR '+remotedir, open(localfile, 'rb'),1024)
        self.ftp.quit()

    def close(self):
        if self.ftp:
            self.ftp.close();



if __name__ == '__main__':
    ftp = FtpClient('127.0.0.1','user','12345',-999)
    ftp.connection()
    ftp.upload("E:\software\FlashFXPNew\Stats.dat","/Documents and Settings/")

