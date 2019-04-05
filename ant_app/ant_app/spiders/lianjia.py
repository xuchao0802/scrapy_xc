# -*- coding: utf-8 -*-
import scrapy
from ant_app.items import lianjia
from urllib import parse


class LianjiaSpider(scrapy.Spider):
    name = 'lianjia'
    allowed_domains = ['lianjia.com']
    start_urls = ['https://hz.lianjia.com/ershoufang/']

    def start_requests(self):
        yield scrapy.Request(url=self.start_urls[0],callback=self.home_page,method="GET",headers=self.get_headers(1))

    def home_page(self, response):
        position = response.css(".position").xpath("./dl[2]/dd/div[1]/div/a")
        total_num = response.css(".leftContent").xpath("./div[2]/h2/span/text()").get()
        if total_num:
            total_num = total_num.strip()
        for i in position:
            first_name = i.xpath("./text()").get()
            url = i.xpath("./@href").get()
            url = parse.urljoin(self.start_urls[0],url)
            meta = {"first_name":first_name,"total_num":total_num}
            yield scrapy.Request(url=url,callback=self.first_url,method="GET",headers=self.get_headers(1),meta=meta)

    def first_url(self, response):
        position = response.css(".position").xpath("./dl[2]/dd/div[1]/div[2]/a")
        first_name = response.meta.get("first_name")
        total_num = response.meta.get("total_num")
        first_num = response.css(".leftContent").xpath("./div[2]/h2/span/text()").get()
        first_url = response.url
        if first_num:
            first_num = first_num.strip()

        for i in position:
            second_name = i.xpath("./text()").get()
            url = i.xpath("./@href").get()
            url = parse.urljoin(self.start_urls[0],url)
            meta = {"first_name":first_name,"total_num":total_num,"first_num":first_num,"second_name":second_name,
                    "first_url":first_url}
            yield scrapy.Request(url=url,callback=self.second_url,method="GET",headers=self.get_headers(1),meta=meta)

    def second_url(self,response):
        first_name = response.meta.get("first_name")
        second_name = response.meta.get("second_name")
        total_num = response.meta.get("total_num")
        first_num = response.meta.get("first_num")
        second_num = response.css(".leftContent").xpath("./div[2]/h2/span/text()").get()
        if second_num:
            second_num = second_num.strip()
        first_url = response.meta.get("first_url")
        second_url = response.url
        item = lianjia()
        item["first_name"] = first_name
        item["second_name"] = second_name
        item["total_num"] = total_num
        item["first_num"] = first_num
        item["second_num"] = second_num
        item["first_url"] = first_url
        item["second_url"] = second_url
        return item

    def parse(self, response):
        pass

    def get_headers(self,type):#返回header
        if type == 1:
            headers = {
                "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
                "Accept-Encoding":"gzip, deflate, br",
                "Accept-Language":"zh-CN,zh;q=0.9",
                "Host":"hz.lianjia.com",
                "User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"

            }
        return headers
