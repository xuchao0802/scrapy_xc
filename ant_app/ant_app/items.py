# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class AntAppItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = scrapy.Field()
    build_data = scrapy.Field()
    index = scrapy.Field()
    url = scrapy.Field()
    cert_code = scrapy.Field()
    flow_no = scrapy.Field()
    set_date = scrapy.Field()
    print_date = scrapy.Field()
    type = scrapy.Field()
    ip = scrapy.Field()

    bank_name = scrapy.Field()
    department = scrapy.Field()
    other_matter = scrapy.Field()
    information_update_time = scrapy.Field()
    company_name = scrapy.Field()
    platform = scrapy.Field()
    signing_time = scrapy.Field()
    online_time = scrapy.Field()
    credit_code = scrapy.Field()
    system_name = scrapy.Field()
    system_version = scrapy.Field()





class onlineloanItem(scrapy.Item):
    # define the fields for your item here like:
    platform = scrapy.Field()#平台名称
    amount = scrapy.Field()#额度
    term = scrapy.Field()#期限
    interest = scrapy.Field()#利率
    phone = scrapy.Field()#电话
    credit = scrapy.Field()#征信
    actual_amount = scrapy.Field()#实际到账
    sort = scrapy.Field()#类别
    material = scrapy.Field()#资料
    characteristic = scrapy.Field()#特点
    number_people = scrapy.Field()#申请人数
    arrival = scrapy.Field()#到帐方式
    speed = scrapy.Field()#放款速度
    review = scrapy.Field()#审核方式
    other = scrapy.Field()
    name = scrapy.Field()#平台名称
    platformname = scrapy.Field()#平台名称
    expense = scrapy.Field()#费用（利率）
    amount_high = scrapy.Field()#额度高低



class AppItem(scrapy.Item):
    # define the fields for your item here like:
    keyword = scrapy.Field()
    apk_md5 = scrapy.Field()
    apk_public_time = scrapy.Field()
    apk_url = scrapy.Field()
    app_downcount = scrapy.Field()
    app_id = scrapy.Field()
    app_name = scrapy.Field()
    author_name = scrapy.Field()
    description = scrapy.Field()
    pkg_name = scrapy.Field()

class lianjia(scrapy.Item):
    first_name = scrapy.Field()
    second_name = scrapy.Field()
    total_num = scrapy.Field()
    first_num = scrapy.Field()
    second_num = scrapy.Field()
    first_url = scrapy.Field()
    second_url = scrapy.Field()


