# -*- coding: utf-8 -*-
import scrapy
import re
from ant_app.items import onlineloanItem

class AikaiwanSpider(scrapy.Spider):
    name = 'aikaiwan'
    allowed_domains = ['www.7177.cn']
    start_urls = ['https://www.7177.cn/daikuanchaoshi']



    def parse(self, response):
        if response.status == 404:
            return None
        number_str = response.css("#daikuan_list").xpath("./tr[11]/td/div/div/label/span/text()").extract()[0]
        page = re.search(r"\d+",number_str).group()

        number = int(page)
        headers = AikaiwanSpider.get_headers(1)
        for i in range(1,number):
            url = "https://www.7177.cn/plugin.php?id=hl_wangdai&page=%d"%i
            yield scrapy.Request(url=url,callback=self.url_parse,method="GET",headers=headers)

    def url_parse(self,response):
        urls = response.css("#daikuan_list").xpath("./tr[@class='filter-tr']")
        headers = AikaiwanSpider.get_headers(2)
        for i in urls:
            url = "https://www.7177.cn" + i.xpath("./td[6]/a/@href").extract()[0]
            yield scrapy.Request(url=url, callback=self.detail_parse, method="GET", headers=headers)

    def detail_parse(self,response):
        container = response.css("div.kn_left.container")
        platform = container.xpath("./div[1]/div[2]/div[1]/span[1]/text()").extract()[0]
        number_people = container.xpath("./div[1]/div[2]/div[2]/table/tbody/tr[1]/td[1]/i/text()").extract()[0]
        amount = container.xpath("./div[1]/div[2]/div[2]/table/tbody/tr[1]/td[2]/i/text()").extract()[0]
        term = container.xpath("./div[1]/div[2]/div[2]/table/tbody/tr[1]/td[3]/i/text()").extract()[0]
        interest = container.xpath("./div[1]/div[2]/div[2]/table/tbody/tr[2]/td[1]/i/text()").extract()[0]
        speed = container.xpath("./div[1]/div[2]/div[2]/table/tbody/tr[2]/td[2]/i/text()").extract()[0]
        review = container.xpath("./div[1]/div[2]/div[2]/table/tbody/tr[2]/td[3]/i/text()").extract()[0]
        arrival = container.xpath("./div[1]/div[2]/div[2]/table/tbody/tr[3]/td[1]/i/text()").extract()[0]
        credit = container.xpath("./div[1]/div[2]/div[2]/table/tbody/tr[3]/td[2]/i/text()").extract()[0]


        other = response.xpath('//*[@id="main-container"]/div[2]/div[2]/div/div[2]/div[1]').xpath("string(.)").extract()[0]
        item = onlineloanItem()
        item["platform"] = platform
        item["amount"] = amount
        item["term"] = term
        item["interest"] = interest
        item["credit"] = credit
        item["arrival"] = arrival
        item["number_people"] = number_people
        item["speed"] = speed
        item["review"] = review
        item["other"] = other
        return item

    def get_headers(type):
        if type == 1:
            headers = {
                "accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
                "accept-encoding": "gzip, deflate, br",
                "accept-language": "zh-CN,zh;q=0.9",
                "referer":"https://www.7177.cn/daikuanchaoshi",
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
