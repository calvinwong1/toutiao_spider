

import requests
from mitmproxy import http, ctx


num = 1788


def request(flow:http.HTTPFlow):
    global num
    # 经测试发现图片url前缀主要是2个
    url = 'http://hm.baidu.com/'

    # response = flow.response
    #
    # info = ctx.log.info
    # info(str(response.text))

    # if flow.request.url.startswith(url):
    #     # 设置视频名
    #     filename = str(num) + '.jpg'
    #     # 使用request获取视频url的内容
    #     # stream=True作用是推迟下载响应体直到访问Response.content属性
    #     res = requests.get(flow.request.url, stream=True)
    #     # print(res)
    #     # 将图片写入文件夹
    #     with open('./im/' + filename, 'wb') as f:
    #         f.write(res.content)
    #     #     print(filename + '下载完成')
    #     # num += 1

