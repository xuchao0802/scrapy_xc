# -*- coding: utf-8 -*-
import scrapy
import re
import json
from ant_app.items import AntAppItem


class XukezhengSpider(scrapy.Spider):
    name = 'xukezheng'
    allowed_domains = ['xukezheng.cbrc.gov.cn']
    start_urls = ['http://xukezheng.cbrc.gov.cn/ilicence/getOrganType.do?_dc=1550250507040']

    def start_requests(self):
        url = self.start_urls[0]
        header = self.get_headers(1)
        yield scrapy.Request(url,callback=self.parse,method="GET",headers=header)

    def parse(self, response):
        headers = self.get_headers(1)
        status = response.status
        json_str = response.text
        json_str = re.sub("([a-zA-Z]+)",r'"\1"',json_str,2)
        data = json.loads(json_str)
        root = data["root"]
        for i in root:
            orgTypeCode =  i["orgTypeCode"]
            orgTypeName = i["orgTypeName"]
            url = "http://xukezheng.cbrc.gov.cn/ilicence/getLicence.do?useState=3&organNo=&fatherOrganNo=&province=&orgAddress=&organType="+orgTypeCode+"&branchType=&fullName=&address=&flowNo="
            if (orgTypeCode != "-1"):
                yield scrapy.FormRequest(url,callback=self.page_parse,formdata={"start":"0","limit":"10"},headers=headers,meta={
                    "orgTypeCode":orgTypeCode,
                    "orgTypeName":orgTypeName
                })


    def page_parse(self,response):
        status = response.status
        response.request
        json_str = response.text
        type = response.meta["orgTypeName"]
        json_str = re.sub("([a-zA-Z]+)", r'"\1"', json_str, 2)
        data = json.loads(json_str)

        totalProperty = data["totalProperty"]
        orgTypeCode = response.meta["orgTypeCode"]
        headers = self.get_headers(1)
        url = "http://xukezheng.cbrc.gov.cn/ilicence/getLicence.do?useState=3&organNo=&fatherOrganNo=&province=&orgAddress=&organType=" + orgTypeCode + "&branchType=&fullName=&address=&flowNo="
        page_number = int(totalProperty/10)
        for i in range(page_number):
            yield scrapy.FormRequest(url, callback=self.detai_parse, formdata={"start": str(10*(i+1)), "limit": "10"},
                                     headers=headers,)

        root = data["root"]
        for i in root:
            item = AntAppItem()
            colIndex = str(i["colIndex"])
            certCode = i["certCode"]
            flowNo = i["flowNo"]
            fullName = i["fullName"]
            setDateStr = i["setDateStr"]
            printDateStr = i["printDateStr"]
            item["index"] = colIndex
            item["cert_code"] = certCode
            item["flow_no"] = flowNo
            item["name"] = fullName
            item["set_date"] = setDateStr
            item["print_date"] = printDateStr
            item["type"] = type
            yield item

    def detai_parse(self,response):
        status = response.status
        json_str = response.body.decode("gbk")
        json_str = re.sub("([a-zA-Z]+)", r'"\1"', json_str, 2)
        data = json.loads(json_str)
        root = data["root"]
        for i in root:
            item = AntAppItem()
            colIndex = str(i["colIndex"])
            certCode = i["certCode"]
            flowNo = i["flowNo"]
            fullName = i["fullName"]
            setDateStr = i["setDateStr"]
            printDateStr = i["printDateStr"]
            item["index"] = colIndex
            item["cert_code"] = certCode
            item["flow_no"] = flowNo
            item["name"] = fullName
            item["set_date"] = setDateStr
            item["print_date"] = printDateStr
            yield item



    def get_headers(self,type):
        if type == 1:
            headers = {
                "Accept-Encoding": "gzip, deflate",
                "Accept-Language": "zh-CN,zh;q=0.9",
                "Referer":"http://xukezheng.cbrc.gov.cn/ilicence/licence/licenceQuery.jsp",
                "User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"
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
