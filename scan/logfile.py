# coding:GBK

# 扫描结果文件保存
# author:wuwh

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


if __name__ == '__main__':
    log = LogFile(fileName="log.txt")
    log.writeLine("你好")
    log.writeLine("hello")
    log.close()

