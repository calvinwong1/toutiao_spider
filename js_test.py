import execjs, time
from selenium import webdriver
from lxml import etree
from selenium.webdriver.common.keys import Keys

class Toutiao(object):

    def __init__(self):
        self.url = 'https://www.toutiao.com'

    def parse(self):
        dr = webdriver.Chrome()
        dr.get(self.url)
        time.sleep(10)
        dr.execute_script("window.scrollBy(0,540)")
        time.sleep(3)
        dr.execute_script("window.scrollBy(0,-200)")
        time.sleep(3)
        dr.execute_script("window.scrollBy(0,800)")
        time.sleep(3)
        dr.execute_script("window.scrollBy(0,-600)")
        time.sleep(3)
        dr.execute_script("window.scrollBy(0,1200)")
        time.sleep(10)
        data = dr.page_source
        # dr.close()
        html = etree.HTML(data)
        title_list = html.xpath('/html/body/div/div[2]/div[2]/div[2]/ul/li/div/div[2]/div/div[1]/a/@href')
        for title in title_list:
            url = 'www.toutiao.com' + title
            print(url)
        time.sleep(50)

if __name__ == '__main__':
    t = Toutiao()
    t.parse()




