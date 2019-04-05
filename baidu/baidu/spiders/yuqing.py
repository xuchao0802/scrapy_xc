# -*- coding: utf-8 -*-
import scrapy
import time
from urllib import parse
import csv
from baidu.items import BaiduItem


class YuqingSpider(scrapy.Spider):
    name = 'yuqing'
    allowed_domains = ['baidu.com']
    #start_urls = ['http://www.baidu.com/']

    def start_requests(self):
        file = "D://data/seeds/wangdaipingtai.csv"
        header,seeds = self.read_csv(file,1)
        for i in seeds:
            company = i#可以数据库或者csv输入
            keyworld = "跑路 失联"
            now_time = time.time()
            last_time = now_time-604800#一周
            meta = {
                "company":company,
                "keyword":keyworld
            }
            url = "https://www.baidu.com/s?q1=&q2="+parse.quote(company)+"&q3="+parse.quote(keyworld)+"&q4=&gpc=stf%3D"\
                  +str(last_time)+"%2C"+str(now_time)+"%7Cstftype%3D1&ft=&q5=&q6=&tn=baiduadv&NR=50"
            yield scrapy.Request(url,method="GET",headers=self.get_headers(),meta=meta)
    def parse(self, response):

        num = 0
        company = response.meta["company"]
        list_content = response.css("#content_left").xpath("./div")
        for i in list_content:
            url = i.css(".t").xpath("./a/@href").get()
            title = i.css(".t").xpath("./a").xpath("string(.)").get()
            summary = i.css(".c-abstract").xpath("string(.)").get()

            item = BaiduItem()

            if url and title and summary:
                num+=1
                item["url"] = url
                item["title"] = title
                item["summary"] = summary
                yield item
        if num <10:
            item1 = BaiduItem()
            item1["error"] = company

            return item1




    def get_headers(self):
        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Cache-Control": "max-age=0",
            "Connection": "keep-alive",
            "Cookie": "BAIDUID=BB749BA62C49137E3B73285D0A4BC605:SL=0:NR=50:FG=1; BIDUPSID=BB749BA62C49137E3B73285D0A4BC605; PSTM=1522377784; MCITY=-179%3A; BD_UPN=13314352; sug=3; sugstore=0; ORIGIN=0; bdime=0; ispeed_lsm=0; ispeed=2; H_PS_PSSID=1443_21110_27509; BDSFRCVID=x6_sJeC62wJCdnc7IFNQjPnPDHdEDlrTH6aoDwXPuluq0xht-py4EG0PjM8g0Ku-LWkcogKKKgOTHI6P; H_BDCLCKID_SF=JJCe_IKMtCvbf40kej-bjICShUFs2U3t-2Q-5KL-MPTrs-JvjUrP3-Pq0MTT0PQJfNQvBfbdJJjoh4jJyf5x2RODWt5ItjbbJ2TxoUJ_MInJhhvGqfvRWJtebPRiB-b9QgbA_ftLJDD5MKKxDjRDbb0sqGuet5-XKKOLVbnVtPOkeq8CDxQI0-LAhNJA0f632HRXbpbFaIbiMC32y5jHhp-WMMTX2Pvt36rxKUoTW4JpsIJMMl_WbT8ULecrLhceaKviahvjBMb1ODQMe6DaDT30DN0s5t3J5-_8oK05HJOoDDv9jln5y4LdjG5fBfJbaDAfalQkLRcmDxJey-OpQ-AX3-Aq54RRbabTLRRa-CJWj--zKbuMQfbQ0M6uqP-jW5IL2U3oKb7JOpvobUnxyMcB0a62btt_tJIjoCoP; SIGNIN_UC=70a2711cf1d3d9b1a82d2f87d633bd8a02917642499; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; delPer=0; BD_CK_SAM=1; PSINO=5; BD_HOME=0; BDRCVFR[fBLL8ZbbiMm]=I67x6TjHwwYf0; H_PS_645EC=fddcGW510mn0%2BRTpdgiEhV0vqz61%2FgFLtSshbfks48ca9y2DjD5FUdTfBRikrRA",
            #"Cookie": "BIDUPSID=7F7F30EAA353F57862E98168A30536AC; PSTM=1547471438; BD_UPN=12314753; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; H_PS_PSSID=1448_21116_28584_28558_28518; sug=0; sugstore=0; ORIGIN=0; bdime=0; BAIDUID=7F7F30EAA353F57862E98168A30536AC:SL=0:NR=20:FG=1; H_PS_645EC=123bcO4J5mJKy7bz0Yzl9Qa0aEYI%2BAeiRlKudYxoAVpANg8VbbEBr%2FekSusSTfE",
            "Host": "www.baidu.com",
            "Upgrade-Insecure-Requests": "1",
            "X-Requested-With":"XMLHttpRequest",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"
        }
        return headers

    def read_csv(sele,file_name, columns):
        data = []
        with open(file_name, "r", encoding="utf-8-sig") as csvfile:
            csv_reader = csv.reader(csvfile)  # 读取csvfile中的文件
            data_header = next(csv_reader)  # 读取第一行每一列的标题 next为读取下一行

            for row in csv_reader:  # 将csv 文件中的数据保存到data中
                data.append(row[columns - 1])  # 选择所需要的数据，###这里可以优化下传入所需的参数进行优化
        return data_header, data
