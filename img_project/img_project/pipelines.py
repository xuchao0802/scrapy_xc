# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exceptions import DropItem
from scrapy.pipelines import images
from scrapy.http import Request


class ImgProjectPipeline(object):
    def process_item(self, item, spider):
        return item


class ImgPipeline(images.ImagesPipeline):
    def get_media_requests(self, item, info):
        url = item["image_urls"]
        yield Request(url,headers=self.get_headers())

    def item_completed(self, results, item, info):
        image_path = [x["path"] for ok,x in results if ok]
        if not image_path:
            raise DropItem("Item contains no images")
        return item

    def get_headers(self,type=1):
        headers = {
                "Host": "img.gsdlcn.com",
                "Connection": "keep-alive",
                "Upgrade-Insecure-Requests": "1",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
                "Accept-Encoding": "gzip, deflate, br",
                "Accept-Language": "zh-CN,zh;q=0.9",
        }
        return headers


