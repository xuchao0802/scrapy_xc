# -*- coding: utf-8 -*-
import scrapy
from ant_app.items import onlineloanItem
import re
import time

from scrapy import Selector
from scrapy.http import HtmlResponse

class OnlineloanSpider(scrapy.Spider):
    name = 'onlineloan'
    custom_settings = {
        "DOWNLOAD_DELAY":"0.5",
        "CONCURRENT_REQUESTS": "10"
    }
    allowed_domains = ['www.zhongxinwanka.com']
    start_urls = ['https://www.zhongxinwanka.com/forum-95-1.html']

    def start_requests(self):
        return [scrapy.Request(self.start_urls[0],headers=self.getHeaders(1))]

    def parse(self, response):

        number_str = response.css("#ct").xpath("./div[3]/div[4]/div/label/span/text()").extract()[0]
        number = re.search("\d+",number_str)
        if number:
            page_number = int(number.group())
        for i in range(2,page_number):
            url = 'https://www.zhongxinwanka.com/forum-95-{}.html'.format(i)
            yield scrapy.Request(url=url,method="GET",callback=self.url_parse,headers=self.getHeaders(1))
        li_list = response.css("#moderate").xpath("./li")
        for i in li_list:
            url = "https://www.zhongxinwanka.com/" + i.xpath("./div[2]/h5/a/@href").extract()[0]

            yield scrapy.Request(url=url, method="GET", callback=self.detail_parse,headers=self.getHeaders(1))

    def url_parse(self, response):
        li_list = response.css("#moderate").xpath("./li")
        for i in li_list:
            url = "https://www.zhongxinwanka.com/"+i.xpath("./div[2]/h5/a/@href").extract()[0]
            yield scrapy.Request( url=url, method="GET", callback=self.detail_parse,headers=self.getHeaders(1))

    def detail_parse(self,response):

        name = response.css("#thread_subject").xpath("./text()").extract()[0]
        tree1 = response.css(".deankviewul")
        amount = tree1.xpath("./li[1]/div/span/text()").extract()[0]
        term = tree1.xpath("./li[2]/div/span/text()").extract()[0]
        expense = tree1.xpath("./li[3]/div/span/text()").extract()[0]
        tree2 = response.css(".deanjkr")
        platformname = tree2.xpath("./ul[1]/li[1]/text()").extract()[0]
        phone = tree2.xpath("./ul[1]/li[3]/text()").extract()[0]
        credit = tree2.xpath("./ul[1]/li[4]/text()").extract()[0]
        actual_amount = tree2.xpath("./ul[1]/li[5]/text()").extract()[0]
        sort = tree2.xpath("./ul[1]/li[6]/text()").extract()[0]
        material = tree2.xpath("./ul[1]/li[7]/text()").extract()[0]
        characteristiclast = tree2.xpath("./ul[2]").xpath("string(.)").extract()[0]
        characteristic = re.sub("\s","",characteristiclast)

        item = onlineloanItem()
        item["name"] = name
        item["amount"] = amount
        item["term"] = term
        item["expense"] = expense
        item["platformname"] = platformname
        item["phone"] = phone
        item["credit"] = credit
        item["actual_amount"] = actual_amount
        item["sort"] = sort
        item["material"] = material
        item["characteristic"] = characteristic

        return item

    def getHeaders(self,type):
        if type == 1:
            headers = {
                "accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
                "accept-encoding": "gzip, deflate, br",
                "accept-language": "zh-CN,zh;q=0.9",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
                "Referer": "https://www.zhongxinwanka.com/",
                "Upgrade-Insecure-Requests": "1",
                "Connection": "keep-alive",
                "Host": "www.zhongxinwanka.com"
            }
        return headers

