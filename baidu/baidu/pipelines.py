# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql

class BaiduPipeline(object):
    def process_item(self, item, spider):
        return item

class LoanPipeline(object):#改需求，将新的字段插入到表中

    template = '''insert into {spider_name}({column})values ({values})'''
    create = '''create table if not exists {spider_name}({columns}); '''
    i = 1
    def __init__(self, settings):
        self.settings = settings

    def process_item(self, item, spider):

        if self.i == 1:
            column_list = []
            for i in item:
                column_list.append("`" + i + "`varchar(40)")
            column = ",".join(column_list)
            self.cursor.execute(self.create.format(spider_name=spider.name,columns=column))
            self.i = 2

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
