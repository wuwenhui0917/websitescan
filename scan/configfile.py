# coding:GBK

# 配置文件类
# author:wuwh

import os.path


class ConfigFile(object):
    def __init__(self):
        self.configname="config.conf"
        self.dict={}
        if not os.path.exists(self.configname):
            pool = 100
            self.dict['poolsize'] = 100
            bindip = "127.0.0.1"
            self.dict['bindip'] = "127.0.0.1"
            bindport = "9999"
            self.dict['port'] = "9999"
            ftpip = '127.0.0.1'
            self.dict['ftpip'] = "127.0.0.1"
            ftpuser = "root"
            self.dict['ftpuser'] = "root"
            ftppwd = 'root'
            self.dict['ftppwd'] = "root"
            ftpdir = "/root"
            self.dict['ftpdir'] = "/root"
            ftplocaldir = "./"
            self.dict['ftplocaldir'] = "./"
            cfile = open(self.configname, "w")
            filecontext = [];
            filecontext.append("poolsize=" + str(pool)+"\n")
            filecontext.append("port=" + str(bindport)+"\n")
            filecontext.append("bindip=" + str(bindip)+"\n")
            filecontext.append("ftpip=" + str(ftpip)+"\n")
            filecontext.append("ftptag=" + "0" + "\n")
            filecontext.append("ftppwd=" + str(ftppwd)+"\n")
            filecontext.append("ftpuser=" + str(ftpuser)+"\n")
            filecontext.append("ftpdir=" + str(ftpdir)+"\n")
            filecontext.append("ftplocaldir=" + str(ftplocaldir)+"\n")
            cfile.writelines(filecontext)
            cfile.close()
        else:
            cfile = open(self.configname,"r")
            for line in cfile:
                liststr = line.split("=")
                self.dict[liststr[0]] = liststr[1]

    def getvalue(self,key):
        return self.dict[key]

    def getStringvalue(self, key):
        str(self.dict[key]).strip()

if __name__ == '__main__':
    config = ConfigFile()
    print str(config.getvalue("ftpdir"))