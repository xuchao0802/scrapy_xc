# -*- coding: utf-8 -*-
import scrapy
from pydispatch import dispatcher
from scrapy import signals
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from ant_app.items import AntAppItem
from urllib import parse


class SeleniumSpider(scrapy.Spider):#这个可以好好改
    name = 'selenium'
    allowed_domains = []
    start_urls = ['https://www.zhihu.com/explore']
    custom_settings = {
        'LOG_LEVEL': 'DEBUG',
        'DOWNLOAD_DELAY': 0,
        'COOKIES_ENABLED': False,  # enabled by default
        'DOWNLOADER_MIDDLEWARES': {
            # 代理中间件
            # 'mySpider.middlewares.ProxiesMiddleware': 400,
            # SeleniumMiddleware 中间件
            'ant_app.middlewares.SeleniumMiddleware': 543,
            # 将scrapy默认的user-agent中间件关闭
            'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
        }
    }

    def __init__(self,settings):
        time_out = settings["SELENIUM_TIMEOUT"]
        window_height = settings["WINDOW_HEIGHT"]
        window_width = settings["WINDOW_WIDTH"]
        self.driver = webdriver.Chrome()
        if window_width and window_height:
            self.driver.set_window_size(window_width,window_height)
        self.driver.set_page_load_timeout(time_out)
        self.wait = WebDriverWait(self.driver,30)
        super(SeleniumSpider, self).__init__()
        #dispatcher.connect(self.spider_close_handle,signals.spider_closed)


    def spider_close_handle(self, spider):
        print(f"mySpiderCloseHandle: enter ")
        self.driver.quit()


    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        settings = crawler.settings
        return cls(settings)

    def start_requests(self):
        url = self.start_urls[0]
        if not url.startswith("http://") and not url.startswith("https://"):
            url = "http://"+url
        yield scrapy.Request(url=url, meta={'usedSelenium': True, 'dont_redirect': True},
                             callback=self.parse)

    def parse(self, response):
        a = response.text
        img_list = response.xpath("//img/@src").getall()

        items = []
        for i in img_list:
            url = response.urljoin(i)
            url1 = parse.urljoin(response.url,url)
            item = AntAppItem()
            item["url"] = url
            items.append(item)
        return items

