import json

import scrapy as scrapy
from scrapy.spiders import CrawlSpider, Rule
import random
import re
import time
from scrapy.spiders import Rule

from scrapy.linkextractors import LinkExtractor


def stringToDict(cookie):
    '''
    将从浏览器上Copy来的cookie字符串转化为Scrapy能使用的Dict
    :return:
    '''
    itemDict = {}
    items = cookie.split(';')
    for item in items:
        key = item.split('=')[0].replace(' ', '')
        value = item.split('=')[1]
        itemDict[key] = value
    return itemDict


# https://read.ixdzs.com/121/121348/p1.html
base_url = 'https://read.ixdzs.com/121/121348/p{page}.html'
page_parten = r'https://read.ixdzs.com/121/121348/p(\d+).html'
partens = [r'跟.*?新.*?最.*?快', r'正.*?版.*?章.*?节', r'正.*?版.*?首.*?发', r'最.*?新.*?章.*?节', ]


class XiaoShuoSipder(CrawlSpider):
    name = 'xiaoshuo'
    spider_chinese_name = "小说下载"
    allowed_domains = ['read.ixdzs.com']
    # start_urls = ['https://read.ixdzs.com/168/168445/p1.html']

    start_page = 1
    end_page = 3346
    xiaoshuo_name = "修真四万年.txt"

    def start_requests(self):
        # for url in self.start_urls:
        url = base_url.format(page=self.start_page)

        yield scrapy.Request(
            url=url, priority=1,
            dont_filter=True,
            callback=self.download_xiaoshuo)

    def download_xiaoshuo(self, response):
        content = response.css('.content::text').extract()
        title = response.css('.line>h1::text').extract_first()
        with open(self.xiaoshuo_name, 'a') as f:
            f.writelines(title)
            for line in content:
                for p in partens:
                    group = re.search(p, line)
                    if group:
                        continue
                f.write(line)
                f.write('\n')
        page = re.search(page_parten, response.url).group(1)
        page = int(page) + 1
        if page <= self.end_page:
            url = base_url.format(page=page)
            yield scrapy.Request(
                url=url, priority=1,
                dont_filter=True,
                callback=self.download_xiaoshuo)
