# coding:GBK
import paramiko
import os
import sys

class FtpClient(object):

    def __init__(self, ftpip, ftpuser, ftppasswd, port=22):
        self.ftpip = ftpip
        self.ftpuser = ftpuser
        self.ftppasswd = ftppasswd
        self.port = port
        self.transport = None
        self.sftp = None

    def connection(self):
        try:
            transport = paramiko.Transport((str(self.ftpip), int(self.port)))
            transport.connect(username=self.ftpuser, password=self.ftppasswd)
            self.transport = transport
            self.sftp = paramiko.SFTPClient.from_transport(self.transport)
        except Exception as e:
            print ("sftp Error:", e)
            if self.transport:
                self.transport.close()
                self.transport = None
            if self.sftp:
                self.sftp.close()
                self.sftp = None
            raise Exception

    def upload(self, localfile, remotedir):
        filename = os.path.basename(localfile)
        remotetempdir = remotedir
        if str(remotedir).endswith("/"):
            remotetempdir = remotetempdir + filename
        # else:
        #     remotetempdir = remotetempdir

        if self.sftp:
            return self.sftp.put(localfile, remotetempdir)

    def close(self):
        if self.sftp:
            self.sftp.close()
        if self.transport:
            self.transport.close()

if __name__ == '__main__':

    if len(sys.argv) != 6:
        print "please use sftpclient  ip username password  localfile(fullname)  remotefile(fullname)"
        exit(1)
    sftp = FtpClient(sys.argv[1], sys.argv[2], sys.argv[3])
    sftp.connection()
    sftp.upload(sys.argv[4], sys.argv[5])
    sftp.close()

    # sftp = FtpClient("192.168.23.147", "wuwenhui", "wuwenhui")
    # sftp.connection()
    # sftp.upload("E:\\tt\\20181009220225.png", "/home/wuwenhui/works/temp/ddd.png")
    # sftp.close()
    # print os.path.basename("C:\Users\Administrator\Desktop\湖北工程\湖北插码\无压缩版hb_sdc_load\hb_sdc_load.js")