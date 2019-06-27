# -*- coding: utf-8 -*-
import json
import re
import time

import scrapy
from ant_app.items import lianjia
from urllib import parse
import pymysql
from scrapy_redis.spiders import RedisSpider
from collections import namedtuple


class LianjiaSpider(RedisSpider):
    name = 'lianjia'
    redis_key = "lianjia:start_urls"#redis
    to_day = time.localtime()
    log_file_path = 'log/scrapy—{}_{}_{}_{}.log'.format(name,to_day.tm_year, to_day.tm_mon, to_day.tm_mday)
    custom_settings = {

        #"LOG_LEVEL": 'WARNING',
        #"LOG_FILE": log_file_path
    }

    # def __init__(self,*args,**kwargs):
    #     self.allowed_domains = 'lijiaddd.com'
    #     # 修改这里的类名为当前类名
    #     super(LianjiaSpider, self).__init__(*args, **kwargs)

    def start_requests(self):

        host = '127.0.0.1'
        user = "root"
        password = "imiss968"
        database = "crawl_schema"
        sql = '''SELECT distinct second_name,second_url FROM crawl_schema.lianjia
where second_num < 3000 and second_url is not null and second_url like "%chengjiao%" limit 2
'''
        connet = pymysql.connect(host=host,user=user,port=3306,db=database,password=password,charset="utf8")
        cur = connet.cursor()
        num = cur.execute(sql)
        headers = [i[0]for i in cur.description]
        for i in range(num):
            data = cur.fetchone()
            data_nametuple = namedtuple("row",headers)
            data = data_nametuple(*data)
            second_name = data.second_name
            url = data.second_url
            yield scrapy.Request(url=url,method="GET",headers=self.get_headers(1),meta={"second_name":second_name})


    def home_page(self, response):#杭州首页页面
        position = response.css(".position").xpath("./dl[2]/dd/div[1]/div/a")
        total_num = response.css(".leftContent").xpath("./div[2]/div[1]/span/text()").get()
        if not total_num:
            total_num = response.css(".leftContent").xpath("./div[2]/h2/span/text()").get()
        if total_num:
            total_num = total_num.strip()
        for i in position:
            first_name = i.xpath("./text()").get()
            url = i.xpath("./@href").get()
            url = parse.urljoin(self.start_urls[0],url)
            meta = {"first_name":first_name,"total_num":total_num}
            yield scrapy.Request(url=url,callback=self.first_url,method="GET",headers=self.get_headers(1),meta=meta)

    def first_url(self, response):#子区域：萧山余杭，页面
        position = response.css(".position").xpath("./dl[2]/dd/div[1]/div[2]/a")
        first_name = response.meta.get("first_name")
        total_num = response.meta.get("total_num")
        first_num = response.css(".leftContent").xpath("./div[2]/div[1]/span/text()").get()
        if not first_num:
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

    def second_url(self,response):#二级子区域：黄龙、闲林页面
        first_name = response.meta.get("first_name")
        second_name = response.meta.get("second_name")
        total_num = response.meta.get("total_num")
        first_num = response.meta.get("first_num")
        second_num = response.css(".leftContent").xpath("./div[2]/div[1]/span/text()").get()
        if not second_num:
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
        second_name = response.meta["second_name"]
        str = response.css(".page-box.fr").xpath("./div/@page-data").get()
        second_num = response.css(".leftContent").xpath("./div[2]/h2/span/text()").get()
        if not second_num:
            second_num = response.css(".leftContent").xpath("./div[2]/div[1]/span/text()").get()
        if second_num:
            second_num = second_num.strip()
        first_name = response.css(".position").xpath("./dl[2]/dd/div[1]/div[1]/a[@class='selected']/text()").get()
        ziquyu = response.css(".position").xpath("./dl[2]/dd/div[1]/div[2]/a[@class='selected']/text()").get()
        meta = {
            "second_name":second_name,
            "second_num":second_num,
            "first_name":first_name,
            "ziquyu":ziquyu

        }
        a = self.detailurl_parse(response,meta)
        for i in a:
            yield i
        try:
            dict_num = eval(str)
            num = dict_num["totalPage"]
        except:
            num = 0
        if num:
            for i in range(2,num+1):
                url = response.url+"pg{}/".format(i)
                yield scrapy.Request(url=url, callback=self.detailurl_parse, method="GET", headers=self.get_headers(1),meta=meta)
    def detailurl_parse(self,response,meta = None):
        if "chengjiao" in response.url:
            li_list = response.css(".listContent").xpath("./li")
        else:
            li_list = response.css(".sellListContent").xpath("./li")
        meta = meta
        print(meta)
        if meta:
            first_name = meta.get("first_name")
            second_name = meta.get("second_name")
            ziquyu = meta.get("ziquyu")
            second_num = meta.get("second_num")
        else:
            first_name = response.meta.get("first_name")
            second_name = response.meta.get("second_name")
            ziquyu = response.meta.get("ziquyu")
            second_num = response.meta.get("second_num")
        for i in li_list:
            detail_url = i.xpath("./div[1]/div[1]/a/@href").get()
            item = lianjia()
            item["first_name"] = first_name
            item["second_name"] = second_name
            item["ziquyu"] = ziquyu
            item["detail_url"] = detail_url
            item["second_num"] = second_num

            yield item#返回item列表
            #yield scrapy.Request(url=url, callback=self.detail, method="GET", headers=self.get_headers(1),meta=response.meta)
    def detail(self,response):#在售
        ziquyu = response.meta["ziquyu"]
        titles = response.css(".title-wrapper").xpath("./div/div[1]")

        title = titles.xpath("./h1/text()").get()
        subtitle = titles.xpath("./div/text()").get()

        overview = response.css(".overview").xpath("./div[2]")

        price = overview.xpath("./div[2]/span[1]/text()").get()
        price_unit = overview.xpath("./div[2]/div[1]/div[1]/span/text()").get()


        cenggao = overview.xpath("./div[3]/div[1]/div[2]/text()").get()
        chaoxiang = overview.xpath("./div[3]/div[2]/div[1]/text()").get()
        ceng = overview.xpath("./div[3]/div[2]/div[2]/text()").get()
        mianji = overview.xpath("./div[3]/div[3]/div[1]/text()").get()
        jianchengshijian = overview.xpath("./div[3]/div[3]/div[2]/text()").get()

        xiaoqu = overview.xpath("./div[4]/div[1]/a[1]/text()").get()
        quyu = overview.xpath("./div[4]/div[2]/span[2]").xpath("string(.)").get()
        kanfangshijian = overview.xpath("./div[4]/div[3]/span[2]/text()").get()
        lianjiaid = overview.xpath("./div[4]/div[4]/span[2]/text()").get()

        information = response.css(".introContent")

        huxin = information.xpath("./div[1]/div[2]/ul/li[1]/text()").get()
        taoneimianji = information.xpath("./div[1]/div[2]/ul/li[5]/text()").get()
        diantibi = information.xpath("./div[1]/div[2]/ul/li[10]/text()").get()
        dianti = information.xpath("./div[1]/div[2]/ul/li[11]/text()").get()
        chanquan = information.xpath("./div[1]/div[2]/ul/li[12]/text()").get()

        guapaishijian = information.xpath("./div[2]/div[2]/ul/li[1]/span[2]/text()").get()
        quanshu =information.xpath("./div[2]/div[2]/ul/li[2]/span[2]/text()").get()
        shangcijiaoyi = information.xpath("./div[2]/div[2]/ul/li[3]/span[2]/text()").get()
        yongtu = information.xpath("./div[2]/div[2]/ul/li[4]/span[2]/text()").get()
        nianxian = information.xpath("./div[2]/div[2]/ul/li[5]/span[2]/text()").get()
        chanquansuoshu = information.xpath("./div[2]/div[2]/ul/li[6]/span[2]/text()").get()
        diyaxinxi = information.xpath("./div[2]/div[2]/ul/li[7]/span[2]/text()").get()
        if diyaxinxi:
            diyaxinxi = re.sub(r"\s+"," ",diyaxinxi)


        fanbenbeifeng = information.xpath("./div[2]/div[2]/ul/li[8]/span[2]/text()").get()
        fanxieid = information.xpath("./div[2]/div[2]/ul/li[9]/span[2]/text()").get()

        tag = response.css(".tags.clear").xpath("./div[2]").xpath("string(.)").get()
        if tag:
            tag = re.sub(r"\s+", " ",tag)
        tese = response.css(".introContent.showbasemore").xpath("string(.)").get()
        if tese:
            tese = re.sub(r"\s+", " ",tese)

        huxin_detail = response.css("#infoList").xpath("./div")
        room_list =[]

        for i in huxin_detail:
            detail1 = i.xpath("./div[1]/text()").get()
            detail2 = i.xpath("./div[2]/text()").get()
            detail3 = i.xpath("./div[3]/text()").get()
            detail4 = i.xpath("./div[4]/text()").get()
            if detail1:
                dict_room = {detail1:[detail2,detail3,detail4]}
                room_list.append(dict_room)
        if room_list:
            room_information = json.dumps(room_list)
        else:
            room_information = ""
        item = lianjia()
        item["title"] = title
        item["subtitle"] = subtitle
        item["price_unit"] = price_unit
        item["price"] = price
        item["cenggao"] = cenggao
        item["chaoxiang"] = chaoxiang
        item["ceng"] = ceng
        item["mianji"] = mianji
        item["jianchengshijian"] = jianchengshijian
        item["xiaoqu"] = xiaoqu
        item["quyu"] = quyu
        item["kanfangshijian"] = kanfangshijian
        item["lianjiaid"] = lianjiaid
        item["huxin"] = huxin
        item["taoneimianji"] = taoneimianji
        item["diantibi"] = diantibi
        item["dianti"] = dianti
        item["chanquan"] = chanquan
        item["guapaishijian"] = guapaishijian
        item["quanshu"] = quanshu
        item["shangcijiaoyi"] = shangcijiaoyi
        item["yongtu"] = yongtu
        item["nianxian"] = nianxian
        item["chanquansuoshu"] = chanquansuoshu
        item["diyaxinxi"] = diyaxinxi
        item["fanbenbeifeng"] = fanbenbeifeng
        item["fanxieid"] = fanxieid
        item["tag"] = tag
        item["tese"] = tese
        item["room_information"] = room_information
        item["ziquyu"] = ziquyu
        return item

    def get_headers(self,type):
        if type == 1:
            headers = {
                "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
                "Accept-Encoding":"gzip, deflate, br",
                "Accept-Language":"zh-CN,zh;q=0.9",
                "Host":"hz.lianjia.com",
                "User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"

            }
        return headers
