# -*- coding: utf-8 -*-
import scrapy
from ant_app.items import onlineloanItem
import re

#redis的代码

from scrapy_redis.spiders import RedisSpider


class KouzidashiSpider(RedisSpider):
    name = 'kouzidashi'
    redis_key = "kouzidashi:start_urls"#redis
    custom_settings = {
        "DOWNLOAD_DELAY":"2",
        "CONCURRENT_REQUESTS":"3"
    }
    allowed_domains = ['www.9889.cn']
    start_urls = ['http://www.9889.cn/']

    def parse(self, response):
        number = response.css(".ui-netloan-head.cl").xpath("./div/span/text()").extract()[0]
        number = int(int(number)/60+1)
        for i in range(1,number+1):
            url = "http://www.9889.cn/forum.php?id=4&page={}".format(i)
            header =self.get_headers(1)
            yield scrapy.Request(url,callback=self.url_parse,method="GET",headers=header)

    def url_parse(self,response):
        url_list = response.css("#content_news_list > section")
        headers = self.get_headers(1)
        for i in url_list:
            name = i.xpath("./li/div[2]/a/text()").extract()[0]
            url = i.xpath("./li/div[2]/a/@href").extract()[0]
            yield scrapy.Request(url,callback=self.detail_parse,method="GET",headers=headers,meta={"name":name,})

    def detail_parse(self,response):
        infor = response.css(".typeoption")
        platform = infor.xpath("./table/tbody/tr[1]/td/text()").extract()[0]
        sort = infor.xpath("./table/tbody/tr[2]/td/text()").extract()[0]
        amount_high = infor.xpath("./table/tbody/tr[3]/td/text()").extract()[0]
        amount = infor.xpath("./table/tbody/tr[4]/td/text()").extract()[0]
        interest = infor.xpath("./table/tbody/tr[5]/td/text()").extract()[0]
        term = infor.xpath("./table/tbody/tr[6]/td/text()").extract()[0]
        characteristic = infor.xpath("./table/tbody/tr[7]/td/text()").extract()[0]
        other_last = response.css("div.t_fsz").xpath("./table/tr/td/font").xpath("string(.)").getall()
        other_last = ";".join(other_last)
        platform = re.sub(r"\s","",platform)
        sort = re.sub(r"\s","",sort)
        amount_high = re.sub(r"\s","",amount_high)
        amount = re.sub(r"\s","",amount)
        interest = re.sub(r"\s","",interest)
        term = re.sub(r"\s","",term)
        characteristic = re.sub(r"\s","",characteristic)
        other = re.sub(r".*?编辑|游客.*?回复|\s","",other_last)
        item = onlineloanItem()
        item["platform"] = platform
        item["sort"] = sort
        item["amount_high"] = amount_high
        item["amount"] = amount
        item["interest"] = interest
        item["term"] = term
        item["characteristic"] = characteristic
        item["other"] = other
        return item


    def get_headers(self,type):
        if type == 1:
            headers = {
                "accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
                "accept-encoding": "gzip, deflate",
                "accept-language": "zh-CN,zh;q=0.9",
                "referer":"https://http://www.9889.cn",
                "Host": "www.9889.cn",
                "upgrade-insecure-requests":"1",
                "user-agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"
            }
        elif type == 2:
            headers = {
                "accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
                "accept-encoding": "gzip, deflate, br",
                "accept-language": "zh-CN,zh;q=0.9",
                "upgrade-insecure-requests":"1",
                "user-agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"
            }
        return headers


