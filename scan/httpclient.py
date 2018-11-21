# coding:GBK
import httplib, urllib
import urlparse


class HttpClient(object):

    def __init__(self,url,timeout=6000):
        self.url = url
        urlinfo = urlparse.urlparse(url)
        if urlinfo.port:
            self.port = int(urlinfo.port)
        else:
            self.port = 80

        self.path = urlinfo.path+"?"+urlinfo.query
        self.host = urlinfo.netloc
        self.timeout = timeout

    def dopost(self, params):
        params = urllib.urlencode(params)
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0'
        }

        httpclient =httplib.HTTPConnection(self.host, port=int(self.port), timeout=self.timeout)

        try:
            httpclient.request("POST", self.path, params, headers)
            response = httpclient.getresponse()
            print(response.status)
            print(response.read())
            response.close()
        except  Exception as e:
            print("处理失败",e)
        finally:
            if httpclient:
                httpclient.close()
if __name__ == '__main__':
    # http = HttpClient("https://www.jd.com")
    # http.dopost({"1111": "22222", "1111": 44444})
    urlinfo = urlparse.parse_qs("wwww=12&33=456")
    print urlinfo.get("wwww")[0]
