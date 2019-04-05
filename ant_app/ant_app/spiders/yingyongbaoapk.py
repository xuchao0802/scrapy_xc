# -*- coding: utf-8 -*-
import scrapy
import json
from urllib import parse
from ant_app.items import AppItem
import re
import pymysql

class YingyongbaoapkSpider(scrapy.Spider):
    name = 'yingyongbao'
    allowed_domains = ['sj.qq.com']
    start_urls = ['http://sj.qq.com/']

    def start_requests(self):
        host = "localhost"
        user = "root"
        password = "imiss968"
        database = "crawl_schema"
        sql = "select distinct platform from aikaiwan limit 500 "  # 插入sql语句
        count = "select count()"
        db = pymysql.connect(host=host, user=user, password=password, db=database, port=3306, charset="utf8")
        cursor = db.cursor()
        cursor.execute(sql)
        i = cursor.rowcount#cursor得到的个数
        t = True
        while t:
            i = cursor.fetchone()
            if i is None:
                t = False
            else:
                keyword = i[0]
                keyword = re.search("\S+", keyword).group()
                url = "https://sj.qq.com/myapp/searchAjax.htm?kw=" + parse.quote(keyword) + "&pns=&sid="
                meta = {"keyword": keyword, "pageNumberStack": "null"}
                yield scrapy.Request(url=url, callback=self.parse, method="GET", meta=meta)  # self.方法名字
        cursor.close()
        db.close()


    def parse(self, response):
        keyword = response.meta["keyword"]
        #page_number_stack = response.meta["pageNumberStack"]
        json_data = json.loads(response.body)
        obj = json_data["obj"]
        page_number_stack_netx = obj["pageNumberStack"]
        #next_url = "https://sj.qq.com/myapp/searchAjax.htm?kw=" + parse.quote(keyword) + "&pns="+parse.quote(page_number_stack_netx)+"&sid=0"

        #has_nest = obj["hasNext"]
        appdetails = obj["appDetails"]
        items = []
        #data = {"kw":keyword,"pns":page_number_stack_netx,"sid":"0"}

        for i in appdetails:
            apk_md5 = i["apkMd5"]
            apk_publishtime = str(i["apkPublishTime"])
            apk_url = i["apkUrl"]
            app_downcount = str(i["appDownCount"])
            app_id = str(i["appId"])
            app_name = i["appName"]
            author_name = i["authorName"]
            description = i["description"]
            pkg_name = i["pkgName"]
            item = AppItem()
            item["keyword"] = keyword
            item["apk_md5"] = apk_md5
            item["apk_public_time"] = apk_publishtime
            item["apk_url"] = apk_url
            item["app_downcount"] = app_downcount
            item["app_id"] = app_id
            item["app_name"] = app_name
            item["author_name"] = author_name
            item["description"] = description
            item["pkg_name"] = pkg_name

            items.append(item)
        '''
        meta = {"keyword": keyword, "pageNumberStack":page_number_stack_netx }
        headers = self.getHeaders(1)
        if(has_nest==1 and page_number_stack != page_number_stack_netx):
            scrapy.FormRequest(url=next_url, callback=self.getapk, method="POST", meta=meta, formdata=data,\
                               headers=headers)'''
        return items

    def get_headers(self, type):
        if (type == 1):
            headers = {
                "": ""
            }
            return headers

'''
with open("d:/data/seeds/data_zhongxinwanka.txt", "r", encoding="utf-8") as f:
    for i in f:
        keyword = re.search("\S+",i).group()
        url = "https://sj.qq.com/myapp/searchAjax.htm?kw="+parse.quote(keyword)+"&pns=&sid="
        meta = {"keyword": keyword, "pageNumberStack": "null"}
        yield scrapy.Request(url=url, callback=self.parse, method="GET", meta=meta)  # self.方法名字
f.close()'''