# -*- coding: utf-8 -*-
import scrapy
from scrapy_redis.spiders import RedisSpider
from urllib.parse import quote,urljoin
from ant_app.items import boss
import time
import re


class BossSpider(RedisSpider):
    name = 'boss'
    allowed_domains = ['www.zhipin.com']
    start_urls = ['http://www.zhipin.com/']
    redis_key = "boss:start_url"

    to_day = time.localtime()
    log_file_path = 'log/scrapy—{}_{}_{}_{}.log'.format(name,to_day.tm_year, to_day.tm_mon, to_day.tm_mday)
    custom_settings = {
        "LOG_LEVEL":'DEBUG',
        #"LOG_FILE":log_file_path
    }
    def make_requests_from_url(self, url):
        return scrapy.Request(url,meta={"name":"world"},callback=self.get_detail)
    '''
    def start_requests(self):#只能return一个request
        keywords = ["爬虫","python"]
        for keyword in keywords:
            a = quote(keyword)
            for num in range(1,11):
                url = "https://www.zhipin.com/c101210100/?query="+a+"&page={}&ka=page-{}".format(num,num)
                yield scrapy.Request(url=url,callback=self.parse,method="GET",dont_filter=True,)'''

    def parse(self, response):
        url_list = response.css(".job-list").xpath("./ul/li")
        for li in url_list:
            url = li.xpath("./div/div[1]/h3/a/@href").get()
            url = urljoin("http://www.zhipin.com/",url)
            yield scrapy.Request(url=url,callback=self.get_detail,method="GET",dont_filter=True)

    def get_detail(self, response):
        url = response.url
        title_ele = response.css(".job-primary.detail-box").xpath("./div")
        job_status = title_ele.xpath("./div[1]/text()").get()
        name = title_ele.xpath("./div[2]/h1/text()").get()
        xinzhi = title_ele.xpath("./div[2]/span/text()").get()
        if xinzhi:
            xinzhi = re.sub(r"\s","",xinzhi)
        information = title_ele.xpath("./p").xpath("string(.)").get()
        fuli = title_ele.xpath("./div[3]/div[1]/div").xpath("string(.)").get()
        if fuli:
            fuli = re.sub(r"\s","",fuli)

        xinxi = response.css("#main").xpath("./div[3]/div/div[2]/div[2]")
        yaoqiu = xinxi.xpath("./div[1]/div").xpath("string(.)").get()
        if yaoqiu:
            yaoqiu = re.sub(r"\s","",yaoqiu)

        gongsijieshao = response.css(".job-sec.company-info").xpath('./div/text()').get()
        if gongsijieshao:
            gongsijieshao = re.sub(r"\s","",gongsijieshao)

        gongsi = response.css(".level-list").xpath('./preceding-sibling::div[1]/text()').get()
        zhucezijin = response.css(".level-list").xpath('./li[2]/text()').get()
        chenglishijian = response.css(".level-list").xpath('./li[3]/text()').get()

        dizhi = response.css(".job-location").xpath("./div[1]/text()").get()
        sider_company = response.css(".sider-company")
        shangshi = sider_company.xpath("./p[2]/text()").get()
        renshu = sider_company.xpath("./p[3]/text()").get()
        hangye = sider_company.xpath("./p[4]/a/text()").get()
        item = boss()
        item["url"] = url
        item["job_status"] = job_status
        item["name"] = name
        item["xinzhi"] = xinzhi
        item["information"] = information
        item["fuli"] = fuli
        item["yaoqiu"] = yaoqiu
        item["gongsijieshao"] = gongsijieshao
        item["gongsi"] = gongsi
        item["zhucezijin"] = zhucezijin
        item["chenglishijian"] = chenglishijian
        item["dizhi"] = dizhi
        item["shangshi"] = shangshi
        item["renshu"] = renshu
        item["hangye"] = hangye
        return item

