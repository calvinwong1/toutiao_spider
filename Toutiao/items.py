# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ToutiaoItem(scrapy.Item):
    # define the fields for your item here like:
    news_title = scrapy.Field()  #标题
    url = scrapy.Field()  #链接
    chinese_tag = scrapy.Field()  #标签
    comments_count = scrapy.Field()  #评论数
    source = scrapy.Field()  #消息来源
    behot_time = scrapy.Field()  #新闻更新时间
    content = scrapy.Field()  #新闻正文 OK
    original = scrapy.Field()  #确认原创 OK
    re_time = scrapy.Field()  #发布时间 OK
    all_html = scrapy.Field()  #整个网页 OK


