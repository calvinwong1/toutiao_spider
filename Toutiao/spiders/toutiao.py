# -*- coding: utf-8 -*-

import scrapy, time, hashlib, json, random, re, js2py
from selenium import webdriver
from Toutiao.items import ToutiaoItem
from lxml import etree
from bs4 import BeautifulSoup


class ToutiaoSpider(scrapy.Spider):
    name = 'toutiao'
    allowed_domains = ['toutiao.com']
    start_urls = ['https://www.toutiao.com/ch/news_hot/']

    list_headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36',
        'accept-language':'zh-CN,zh;q=0.9',
        # 'cookie':'tt_webid=6579822068031849992; WEATHER_CITY=%E5%8C%97%E4%BA%AC; UM_distinctid=164b15fe2895b6-01607aa9d62a44-3c3c5905-15f900-164b15fe28a274; tt_webid=6579822068031849992; csrftoken=94bfdd489924cccbfbbe31dc202345af; uuid="w:3a6cfdf8bfac4d8aadb455ca296a4a61"; _ga=GA1.2.1690684185.1532049199; _gid=GA1.2.704895689.1532049199; __tasessionId=9klfhw5i31532075904460; CNZZDATA1259612802=1379682853-1531979245-https%253A%252F%252Fwww.baidu.com%252F%7C1532071047',
    }

    detail_headers = {
        'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36',
        'upgrade-insecure-requests': '1',
        'accept-language': 'zh-CN,zh;q=0.9',
        'accept-encoding': 'gzip, deflate, br',
    }

    def parse(self, response):

        # '''https://www.toutiao.com/api/pc/feed/?category=news_hot&utm_source=toutiao&widen=1&max_behot_time={}&max_behot_time_tmp={}&tadrequire=true&as={}&cp={}&_signature={}'''

        # print(response.url)

        # print(type(now))
        # chrom = webdriver.ChromeOptions()
        # chrom.add_argument('--proxy-server=http://125.46.0.62:53281')
        # dr = webdriver.Chrome(chrome_options=chrom)
        dr = webdriver.Chrome()
        dr.get(response.url)
        time.sleep(3)
        now = int(time.time())
        print('now:', now)
        url_list = []
        pp = 0
        while pp <= 2:
            js_code = 'return TAC.sign({})'.format(str(now))
            signature = str(dr.execute_script(js_code))

            """as: "A1" + s + e.slice(-3),
            cp: e.slice(0, 3) + r + "E1" 
            dr = webdriver.Chrome()
            dr.get(start_urls[0])

            if (8 != e.length)
            return {
                as: "479BB4B7254C150",
                cp: "7E0AC8874BB0985"
            };

            for (var n = i.slice(0, 5), a = i.slice(-5), s = "", o = 0; 5 > o; o++)
                s += n[o] + e[o];
            for (var r = "", c = 0; 5 > c; c++)
                r += e[c + 3] + a[c];

            e = t.toString(16).toUpperCase()

            i = md5(t).toString().toUpperCase()

            t = Math.floor((new Date).getTime() / 1e3)
            toUpperCase():将字母变大
            """


            #计算出ｔ的值
            t = now
            # print('t:',t)

            #进行hash运算，并计算公式：i = md5(t).toString().toUpperCase()
            md5 = hashlib.md5()
            md5.update(str(t).encode())
            hs = md5.hexdigest()
            # print('--------------',hs)
            i = hs.upper()
            # print('i:',i)

            #计算公式：e = t.toString(16).toUpperCase()
            e = (str(hex(t))).upper()[2:]
            # print('===========',e)


            #计算公式：n = i.slice(0, 5), a = i.slice(-5)
            n = i[0:5]
            # print('n:',n)
            a = i[-5:]
            # print('a:',a)

            s = ""
            for o in range(5):
                s += str(n[o] + e[o])
            # print('s:', s)

            # print(s)

            r = ""
            for c in range(5):
                r += str(e[c + 3] + a[c])
            # print('r:', r)

            if len(e) != 8:
                a_s = '479BB4B7254C150'
                cp = '7E0AC8874BB0985'

            #as: "A1" + s + e.slice(-3)
            a_s = "A1" + s + e[-3:]
            # print("as:",a_s)

            #cp: e.slice(0, 3) + r + "E1"
            cp = e[0:3] + r + "E1"
            # print('cp:',cp)

            get_url = 'https://www.toutiao.com/api/pc/feed/?category=news_hot&utm_source=toutiao&widen=1&max_behot_time={}&max_behot_time_tmp={}&tadrequire=true&as={}&cp={}&_signature={}'.format(str(now), str(now), a_s, cp, signature)
            print(get_url)
            now -= random.randint(1800, 3600)
            # time.sleep(3)
            print(now)
            pp += 1
            url_list.append(get_url)
            # time.sleep(1)
        dr.close()
        for url in url_list:
            yield scrapy.Request(url, callback=self.parse_data, headers=self.list_headers)

    def parse_data(self, response):
        # time.sleep(3)
        # print(response.url)
        dict_data = json.loads(response.body.decode())
        # print(dict_data)
        i = 0
        for data in dict_data['data']:
            item = ToutiaoItem()

            if '/group/' in data['source_url']:
                try:
                    item['url'] = "https://www.toutiao.com" + data['source_url']
                    item['news_title'] = data['title']
                    item['chinese_tag'] = data['chinese_tag']
                    item['comments_count'] = data['comments_count']
                    item['source'] = data['source']
                    item['behot_time'] = data['behot_time']  #新闻刷新时间
                except:
                    item['comments_count'] = None
                    item['chinese_tag'] = None
                    item['source'] = None
                print(item)
                i += 1
                print(i)
                yield scrapy.Request(url=item['url'], headers=self.detail_headers,callback=self.parse_detail_data, meta={'meta': item}, dont_filter=True)

            # if '/group/' in data['source_url']:
            #     url = "https://www.toutiao.com" + data['source_url']
            #     news_title = data['title']
            #     print(news_title)
            #     if data['chinese_tag']:
            #         chinese_tag = data['chinese_tag']
            #     else:
            #         chinese_tag = None
            #     print(chinese_tag)
            #     if data['comments_count']:
            #         comments_count = data['comments_count']
            #     else:
            #         comments_count = None
            #     if data['source']:
            #         source = data['source']
            #     else:
            #         source = None
            #     behot_time = data['behot_time']  #新闻刷新时间
            #
            #     meta = {
            #         "news_title" : news_title,
            #         "url" : url,
            #         "chinese_tag" : chinese_tag,
            #         "comments_count" : comments_count,
            #         "source" : source,
            #         "behot_time": behot_time,
            #     }

                # yield scrapy.Request(url=meta['url'], headers=self.detail_headers,callback=self.parse_detail_data, meta={'meta':meta}, dont_filter=True)


    def parse_detail_data(self, response):
        item = response.meta['meta']
        data = response.body.decode()
        item['all_html'] = data
        # if 'https://www.toutiao.com/' in item['url']:
        #     print(item['url'])
        pa = re.findall(r'<script>(var BASE_DATA =\s.*?)</script>', data, re.S)
        # res = pa.search(data)
        # print(pa)
        #判断是头条站内的
        if pa:
            js_data = js2py.eval_js(pa).to_dict()
            #获取页面数据
            art = js_data.get('articleInfo')
            #正文
            content = art.get('content').replace('&lt;', '').replace('p&gt;', '').replace('div&gt;', '').replace('strong&gt;', '').replace('&quot;', '').replace('blockquote&gt;', '').replace('div class&#x3D;pgc-img&gt;img src&#x3D;', '').replace('img_width&#x3D;', '').replace('img_height&#x3D;', '').replace('alt&#x3D;', '').replace('inline&#x3D;0&gt;p class&#x3D;pgc-img-caption&gt;', '').replace('inline&#x3D;0&gt;', '')
            # item['content'] = content
            # rel_content = re.sub('/([A-Z])/g','',content)
            #是否原创
            original = art.get('subInfo').get('isOriginal')
            # item['original'] = art.get('subInfo').get('isOriginal')
            #发布时间
            re_time = art.get('subInfo').get('time')
            # item['re_time'] = art.get('subInfo').get('time')
            print(original)
            print(content)
            print(re_time)
        else:
        #重定向后的判断
            # pattern = re.compile(r'<p>(.*?)</p>', re.S)
            # all_data = re.findall(pattern,data)[0]

            #看需求需不需要加original
            soup = BeautifulSoup(data, 'html.parser')
            if soup.find('time'):
                # item['re_time'] = soup.find('time').get_text()
                time = soup.find('time').get_text()
                print(time)
            elif soup.find('span', {'class': 'time'}):
                # item['re_time'] = soup.find('span', {'class': 'time'}).get_text()
                time = soup.find('span', {'class': 'time'}).get_text()
                print(time)
            #获取正文
            for p in soup.find_all('p'):
                if p.get_text():
                    content = p.get_text().strip()
                    # item['content'] = p.get_text().strip()
                    print(content)


