import random

import requests
import json
import time
import hashlib
from selenium import webdriver



class Toutiao(object):
    def __init__(self):
        self.headers ={
            # 'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.119 Safari/537.36',
            'User-Agent':'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; MyIE2)',
            # 'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/18.0.1025.166 Safari/537.17',
            # 'Referer':'https://www.toutiao.com/ch/funny/',
            'cookie':'tt_webid=6556340440634754564; WEATHER_CITY=%E5%8C%97%E4%BA%AC; tt_webid=6556340440634754564; UM_distinctid=1636b809f960-0e1b91bffc352b-3e3d560e-100200-1636b809f981a5; uuid="w:26be8e906f944889bd823ba841ec4db6"; _ga=GA1.2.1171737800.1526553047; _gid=GA1.2.1110732549.1526890393; tt_track_id=b1768c7b9bd1aa82a43b61dd3a7f02e7; CNZZDATA1259612802=689798145-1526516157-https%253A%252F%252Fwww.baidu.com%252F%7C1527120790; __tasessionId=efr1d5k1d1527123255664',
            'upgrade-insecure-requests':'1',
            'cache-control':'max-age=0',
            'accept-language':'zh-CN,zh;q=0.9',
            'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            # ':scheme':'https',
            # ':path':'/api/pc/feed/?category=funny&utm_source=toutiao&widen=1&max_behot_time=1527113799&max_behot_time_tmp=1527113799&tadrequire=true&as=A185AB20F52E847&cp=5B058E4834876E1&_signature=MK9TvgAAa6.M1rnC1DEUhTCvU6',
            # ':method':'GET',
            # ':authority':'www.toutiao.com',
        }
        self.file = open('toutiao_funny.json', 'w', encoding='utf-8')
        self.url = 'https://www.toutiao.com/api/pc/feed/?category=funny&utm_source=toutiao&widen=1&max_behot_time={}&max_behot_time_tmp={}&tadrequire=true&as={}&cp={}&_signature={}'
        print(self.url)
        self.url_selenium = 'https://www.toutiao.com/ch/funny/'
        self.JavascriptExecutor = webdriver.Chrome()
        self.JavascriptExecutor.get(self.url_selenium)

    def get_time_as_cp_signature(self,time):
        url_dict = {}
        t = time
        print(t)
        url_dict['max_behot_time'] = str(t)  # 得到'max_behot_time'
        url_dict['max_behot_time_tmp'] = str(t)  # 得到'max_behot_time_tmp'

        js_code = "return TAC.sign({})".format(t)
        signature = self.JavascriptExecutor.execute_script(js_code)  # 得到'_signature'
        url_dict['_signature'] = str(signature)

        e = str(hex(t)).upper()[2:]

        # 创建hash对象
        md5 = hashlib.md5()
        # 将需要做hash运算的字符串添加进对象中,python3中待hash的字符串需要bytes类型
        md5.update(str(t).encode())
        # 获取hash运算结果
        i = str(md5.hexdigest()).upper()

        if len(e) != 8:
            url_dict['as'] = "479BB4B7254C150"
            url_dict['cp'] = "7E0AC8874BB0985"
            return url_dict

        n = i[0:5]
        a = i[-5:]
        s = ''
        o = 0
        while o < 5:
            s += n[o] + e[o]
            o += 1

        r = ''
        c = 0
        while c < 5:
            r += e[c + 3] + a[c]
            c += 1

        as_str = "A1" + s + e[-3:]
        url_dict['as'] = as_str  # 得到'as'

        cp_str = e[0:3] + r + "E1"
        url_dict['cp'] = cp_str  # 得到'cp'

        return url_dict

    def generate_url(self,url,url_dict):
        return self.url.format(url_dict['max_behot_time'],url_dict['max_behot_time_tmp'],url_dict['as'],url_dict['cp'],url_dict['_signature'])

    def get_data(self,url):
        response = requests.get(url, headers=self.headers)
        # print(response.status_code)
        return response.content.decode()

    def parse_data(self,response):
        print(type(response))
        dict_data = json.loads(response)
        news_list = []
        for news in dict_data["data"]:
            temp = {}
            temp["title"] = news["title"]
            temp["url"] = 'https://www.toutiao.com/' + 'a' + news["item_id"]
            news_list.append(temp)
        return news_list

    def save_data(self, news_list):
        # print(news_list)
        for data in news_list:
            # print(data)
            result = json.dumps(data, ensure_ascii=False) + ',\n'
            self.file.write(result)
        #每写一页数据就来一次换行
        self.file.write('\n')

    def __del__(self):
        self.file.close()

    def run(self):
        i = 0
        send_time = int(time.time())
        print(send_time)
        while True:
            # 得到time,as,cp,签名
            url_dict = self.get_time_as_cp_signature(send_time)
            # 拼接用请求的url
            url = self.generate_url(self.url,url_dict)
            print(url)
            #请求url，得到响应的数据
            response_data = self.get_data(url)
            #解析相应的数据，提取需要的内容
            news_list = self.parse_data(response_data)
            #保存数据
            self.save_data(news_list)
            # 每隔2秒翻一页，爬10页
            send_time -= random.randint(1800,3600) #越往下翻页，需要的时间越早，大概每30mins-60mins有新新闻产生，保证内容不重复
            time.sleep(2)
            i += 1
            if i == 10:
                break
        #关闭selenium的webdriver
        self.JavascriptExecutor.close()

# '1527062238','2018-05-23 15:57:18'
# '1527060438','2018-05-23 15:27:18'
# '1800','30mins'

if __name__ == '__main__':
    toutiao = Toutiao()
    toutiao.run()