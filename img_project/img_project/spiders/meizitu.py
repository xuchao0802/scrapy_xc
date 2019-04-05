# -*- coding: utf-8 -*-
import logging

import scrapy
from img_project.items import ImgProjectItem


class MeizituSpider(scrapy.Spider):
    name = 'meizitu'
    allowed_domains = ['meizitu.com']
    start_urls = ['https://www.mzitu.com/']

    def start_requests(self):
        url = self.start_urls[0]
        yield scrapy.Request(url,headers=self.get_headers(1))

    def parse(self, response):
        url_list = response.css(".postlist").xpath("./ul/li")
        for i in url_list:
            item = ImgProjectItem()
            url = i.xpath("./a/@href").get()
            img_url = i.xpath("./a/img/@data-original").get()
            item["url"] = url
            item["image_urls"] = img_url
            yield item




    def get_headers(self,type=1):
        headers = {
                "Host": "www.mzitu.com",
                "Connection": "keep-alive",
                "Upgrade-Insecure-Requests": "1",
                "User-Agent": "Mozilla/5.0ct (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
                "Accept-Encoding": "gzip, deflate, br",
                "Accept-Language": "zh-CN,zh;q=0.9"
        }
        return headers

