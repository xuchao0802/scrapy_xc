# -*- coding: utf-8 -*-
import scrapy
import re
from ant_app.items import AntAppItem

class ThirdpaySpider(scrapy.Spider):
    name = 'thirdpay'
    allowed_domains = ['www.pbc.gov.cn']
    start_urls = ['http://www.pbc.gov.cn/zhengwugongkai/127924/128041/2951606/1923625/1923629/index.html']

    def start_requests(self):

        url = ('http://www.pbc.gov.cn/zhengwugongkai/127924/128041/2951606/1923625/1923629/index.html')
        return [scrapy.Request(url=url, callback=self.first_parse, method="POST")]

    def first_parse(self, response):
        # cookie = response
        print(response)
        number_str = response.css(".Normal")
        number_str1 = number_str.xpath("./text()").extract()[1]
        patter = re.compile(r"(\d+)")
        number = patter.search(number_str1).group()
        a = int(number)

        for i in range(1, a + 1):
            url = ("http://www.pbc.gov.cn/zhengwugongkai/127924/128041/2951606/1923625/1923629/d6d180ae/index%d.html" % i)
            yield scrapy.Request(url=url, callback=self.parse, method="POST")

    def parse(self, response):
        divlist = response.css("#d6d180ae830740258523efcbbb6eefae").xpath("./div[2]/table/tbody/tr[2]/td/table")

        items = []

        for i in divlist:
            item = AntAppItem()
            index = i.xpath("./tbody/tr/td[2]/text()").extract()[0]
            name = i.xpath("./tbody/tr/td[3]/font/a/text()").extract()[0]
            data = i.xpath("./tbody/tr/td[4]/text()").extract()[0]

            item["index"] = index
            item["name"] = name
            item["build_data"] = data

            items.append(item)

        return items



    def get_headers(self, i):
        if (i == 0):
            headers = {
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
                "Accept-Encoding": "gzip, deflate",
                "Accept - Language": "zh - CN, zh;q = 0.9",
                "Cache - Control": "max - age = 0",
                "Connection": "keep - alive"
            }
            return headers
        elif (i == 1):
            headers = {
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
                "Accept-Encoding": "gzip, deflate",
                "Accept - Language": "zh - CN, zh;q = 0.9",
                "Cache - Control": "max - age = 0",
                "Connection": "keep - alive"
            }
            return headers