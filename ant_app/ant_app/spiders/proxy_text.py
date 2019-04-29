# -*- coding: utf-8 -*-
import scrapy
from ant_app.items import AntAppItem
import scrapy_redis

class ProxyTextSpider(scrapy.Spider):
    name = 'proxy_text'
    #allowed_domains = ['ip.filefab.com']
    start_urls = ['https://www.xicidaili.com/nn']

    def start_requests(self):
        url =self.start_urls[0]
        yield scrapy.Request(url=url,method="GET",headers=self.get_headers(1))

    def parse(self, response):
        ip_list = response.css("#ip_list").xpath("./tr")
        for i in ip_list:
            ip = i.xpath('./td[2]/text()').get()
            port = i.xpath('./td[3]/text()').get()
            scheme = i.xpath("./td[6]/text()").get()
            if ip and port and scheme:
                url = str.lower(scheme)+"://"+ip+":"+port
                item = AntAppItem()
                item["ip"] = url
                meta = {
                    "proxy":url,
                    "dont_retry":True
                }
                yield scrapy.Request(url="https://www.baidu.com",callback=self.test_pase,meta=meta,dont_filter=True)

    def test_pase(self,response):
        url = response.meta["proxy"]
        item = AntAppItem()
        item["ip"] = url

        return item

    def get_headers(self,type):
        if type == 1:
            headers = {
                "accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
                "accept-encoding": "gzip, deflate, br",
                "accept-language": "zh-CN,zh;q=0.9",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
                "Upgrade-Insecure-Requests": "1",
                "Connection": "keep-alive",
                "Host": "www.xicidaili.com"
            }
        return headers


