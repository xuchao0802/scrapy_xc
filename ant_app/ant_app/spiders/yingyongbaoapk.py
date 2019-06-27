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
    custom_settings = {"CONCURRENT_REQUESTS":16,
                       "DOWNLOAD_DELAY":0,
                       }
    start_urls = ['http://sj.qq.com/']

    def start_requests(self):
        sql = "select distinct platform from aikaiwan limit 50"  #插入sql语句
        a = self.seeds_frommysql(sql)
        for keyword in a:
            keyword = re.search("\S+", keyword).group()
            url = "https://sj.qq.com/myapp/searchAjax.htm?kw=" + parse.quote(keyword) + "&pns=&sid="
            meta = {"keyword": keyword, "pageNumberStack": "null"}
            yield scrapy.Request(url=url, callback=self.parse, method="GET", meta=meta)

    def parse(self, response):
        keyword = response.meta["keyword"]
        #page_number_stack = response.meta["pageNumberStack"]
        json_data = json.loads(response.body)
        obj = json_data["obj"]
        #page_number_stack_netx = obj["pageNumberStack"]
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
            yield scrapy.FormRequest(url=next_url, callback=self.getapk, method="POST", meta=meta, formdata=data,headers=headers)'''
        return items

    def seeds_frommysql(self,sql):
        host = self.settings.get("MYSQL_HOST")
        user = self.settings.get("MYSQL_USER")
        password = self.settings.get("MYSQL_PASSWD")
        database = self.settings.get("MYSQL_DBNAME")
        port = self.settings.get("MYSQL_PORT")
        db = pymysql.connect(host=host, user=user, password=password, db=database, port=port, charset="utf8")
        cursor = db.cursor()
        cursor.execute(sql)
        for i in cursor.fetchall():
            keyword = i[0]
            yield keyword  # self.方法名字
        cursor.close()
        db.close()

    def get_headers(self,num):
        if num == 1:
            headers = {
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
                "Accept-Encoding": "gzip, deflate, br",
                "Accept-Language": "zh-CN,zh;q=0.9",
                "Connection":"keep-alive",
                "Host": "hz.lianjia.com",
                "Upgrade-Insecure-Requests":"1",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
            }
        return headers
