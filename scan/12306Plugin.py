# coding:utf-8
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

checi = "G123"
diriver = webdriver.Chrome()
diriver.get("https://kyfw.12306.cn/otn/leftTicket/init")


# form = diriver.find_element(By.ID,"fromStationText")
# form.send_keys(str(""))
# form.send_keys(str("xian"))
# to = diriver.find_element(By.ID,"toStationText")
# to.send_keys(str(""))
# to.send_keys(str("nanjing"))
# startDate = diriver.find_element(By.ID,"train_date")
# startDate.send_keys("2013-06-07")


def start():
    while True:
        try:
          # diriver.get("https://kyfw.12306.cn/otn/leftTicket/init")
          # time.sleep(3)
          result = find_ticket()
          if result==1:
              print u"抢票成功，请注意支付"
              return
        except:
          print "error"
          time.sleep(3)

        print 'ooo'




def find_ticket():

    button = diriver.find_element(By.ID, "query_ticket")
    button.click()
    time.sleep(2)
    # tableinfo = diriver.find_element(By.ID,"queryLeftTable")
    # print tableinfo
    rows = diriver.find_elements(By.TAG_NAME, "tr")
    for row in rows:
        # print "id==========="+row.get_attribute("id")
        tds = row.find_elements(By.TAG_NAME, "td")
        # print len(tds)
        if len(tds) == 13:
            aele = tds[0].find_element(By.CLASS_NAME,"number")
            # print str(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")+aele.text
            if aele!=None and aele.text==checi:
                print ">>>>>>>>>>>>>>>>>"+tds[3].text
                if tds[3].text != u'--' and tds[3].text != u'无':
                    print 'oklllllllll'
                    tds[12].find_element(By.TAG_NAME, "a").click()
                    reloadcount=0
                    # 进入到订单页面
                    while diriver.current_url != "https://kyfw.12306.cn/otn/confirmPassenger/initDc":
                        if reloadcount==60:
                            return;
                        reloadcount=reloadcount+1
                        time.sleep(1)
                    time.sleep(5)
                    ren = diriver.find_element(By.ID, "normalPassenger_0")
                    ren.click()
                    time.sleep(1)
                    # 提交订单
                    diriver.find_element(By.ID, "submitOrder_id").click()
                    time.sleep(1)
                    # 核对信息
                    diriver.find_element(By.ID, "qr_submit_id").click()
                    while (str(diriver.current_url).index("/payOrder/init")) == -1:
                        time.sleep(1)

                    print "抢票成功"
                    # 关闭
                    diriver.close()
                    return 1

    print row
    return 0

if __name__ == '__main__':
    strpasswprd = raw_input("登陆成功后请按任意键: ")
    start()