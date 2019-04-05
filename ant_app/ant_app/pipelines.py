# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql

class AntAppPipeline(object):
    def process_item(self, item, spider):
        return item


class LoanPipeline(object):#改需求，自动将传入的item插入到数据库中
    yingyongbao = '''insert into yingyongbao(keyword,apk_md5,apk_publishtime,apk_url,app_downcount,app_id,app_name,author_name,description,pkg_name)
                        values('{keyword}','{apk_md5}','{apk_public_time}','{apk_url}','{app_downcount}',
                        '{app_id}','{app_name}','{author_name}','{description}','{pkg_name}')'''
    template = '''insert into {spider_name}({column})values ({values})'''
    create = '''create table if not exists {spider_name}({columns}); '''
    i = 1
    def __init__(self, settings):
        self.settings = settings

    def process_item(self, item, spider):

        if self.i == 1:
            column_list = []
            for i in item:
                column_list.append("`" + i + "`varchar(200)")
            column = ",".join(column_list)
            self.cursor.execute(self.create.format(spider_name=spider.name,columns=column))
            self.i = 2

        if spider.name == "yingyongbaoapkhh":
            sqltext = self.yingyongbao.format(
                keyword=pymysql.escape_string(item['key_world']),
                apk_md5=pymysql.escape_string(item['apk_md5']),
                apk_public_time=item['apk_public_time'],
                apk_url=pymysql.escape_string(item['apk_url']),
                app_downcount=item['app_down_count'],
                app_id=pymysql.escape_string(item['app_id']),
                app_name=pymysql.escape_string(item['app_name']),
                author_name=pymysql.escape_string(item['author_name']),
                description=pymysql.escape_string(item['description']),
                pkg_name=pymysql.escape_string(item['pkg_name']))
            # spider.log(sqltext)
            self.cursor.execute(sqltext)
        else :
            str_list = []
            column_list =[]
            for i in item:
                column_list.append("`" + i + "`")
                str_list.append("'" + item[i] + "'")
            column = ",".join(column_list)
            values = ",".join(str_list)
            sqltext = self.template.format(spider_name=spider.name,column=column,values=values)
            self.cursor.execute(sqltext)
        #else:
            #spider.log('Undefined name: %s' % spider.name)
            #pymysql.escape_string()mysql的格式

        return item

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    def open_spider(self, spider):
        # 连接数据库
        self.connect = pymysql.connect(
            host=self.settings.get('MYSQL_HOST'),
            port=3306,
            db=self.settings.get('MYSQL_DBNAME'),
            user=self.settings.get('MYSQL_USER'),
            passwd=self.settings.get('MYSQL_PASSWD'),
            charset='utf8',
            use_unicode=True,
            cursorclass=pymysql.cursors.DictCursor#使用dictcursor游标是一次性将数据加载到内存中还可以使用pymysql.cursors.SSCursor流式游标
        )
# 通过cursor执行增删查改
        self.cursor = self.connect.cursor()
        self.connect.autocommit(True)

    def close_spider(self, spider):
        self.cursor.close()
        self.connect.close()