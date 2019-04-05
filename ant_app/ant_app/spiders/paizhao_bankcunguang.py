# -*- coding: utf-8 -*-
import scrapy
from ant_app.items import AntAppItem
import re

class BankcunguangSpider(scrapy.Spider):
    name = 'bankcunguang'
    allowed_domains = ['dp.nifa.org.cn']
    start_urls = ['https://dp.nifa.org.cn/HomePage?method=getCapitalInfo']

    def parse(self,response):
        num = response.css("#orgdiv").xpath("./p/font/text()").get()
        ""
        for i in range(1,int(int(num.strip())/6)+2):
            url = "https://dp.nifa.org.cn/HomePage?method=getCapitalInfo&currentPage="+str(i)
            yield scrapy.Request(url,callback=self.page_parse,method="get")

    def page_parse(self, response):
        select_list = response.css("#jigou").xpath("./li")

        for i in select_list:

            url = i.xpath("./div[3]/a/@href").get()
            url = "https://dp.nifa.org.cn"+url
            yield scrapy.Request(url,callback=self.detail_parse,method="get")
    def detail_parse(self,response):

        yinhang = response.css(".intro-txt").xpath("./span[1]/text()").get()
        bumeng = response.css(".intro-txt").xpath("./span[2]/text()").get()
        other = response.css(".intro-txt").xpath("./span[3]").xpath("string(.)").get()
        time = response.css(".intro-txt").xpath("./span[4]/text()").get()
        yinhang = re.sub("\s","",yinhang)
        bumeng = re.sub("\s","",bumeng)
        other = re.sub("\s","",other)
        time = re.sub("\s","",time)

        select_css = response.css("#base-info").xpath("./table/tbody/tr")
        for i in select_css:
            item = AntAppItem()
            company_name = i.xpath("./td[2]/a/text()").get()
            platform = i.xpath("./td[3]/text()").get()
            signing_time = i.xpath("./td[4]/text()").get()
            online_time = i.xpath("./td[5]/text()").get()
            credit_code = i.xpath("./td[6]/text()").get()
            system_name = i.xpath("./td[7]/text()").get()
            system_version = i.xpath("./td[8]/text()").get()



            if company_name != None:
                company_name = re.sub("\s", "", company_name)
                platform = re.sub("\s", "", platform)
                signing_time = re.sub("\s", "", signing_time)
                online_time = re.sub("\s", "", online_time)
                credit_code = re.sub("\s", "", credit_code)
                system_name = re.sub("\s", "", system_name)
                system_version = re.sub("\s", "", system_version)

                item["bank_name"] = yinhang
                item["department"] = bumeng
                item["other_matter"] = other
                item["information_update_time"] = time
                item["company_name"] = company_name
                item["platform"] = platform
                item["signing_time"] = signing_time
                item["online_time"] = online_time
                item["credit_code"] = credit_code
                item["system_name"] = system_name
                item["system_version"] = system_version

                yield item
