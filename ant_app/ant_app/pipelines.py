# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql

class AntAppPipeline(object):
    def process_item(self, item, spider):
        return item


class MysqlPipeline(object):
    template = '''insert into {spider_name}({column})values ({values});'''
    create = '''create table if not exists {spider_name}({columns}); '''
    select = '''select * from {} limit 1; '''
    alter = '''ALTER TABLE `{spider_name}` ADD COLUMN `{columns}` VARCHAR({num}) null;'''

    first = 1
    def __init__(self, settings):
        self.settings = settings

    def process_item(self, item, spider):

        if self.first == 1:
            column_list = []

            for i,y in item.items():
                len_num = len(y)
                len_num = max(len_num*2,100)
                column_list.append("`" + i + "`varchar({})".format(len_num))
            column = ",".join(column_list)
            self.cursor.execute(self.create.format(spider_name=spider.name,columns=column))
            self.cursor.execute(self.select.format(spider.name))
            headers = self.cursor.description
            headers = [i[0] for i in headers]
            for i,y in item.items():
                len_num = len(y)
                len_num = max(len_num*2,100)
                if i not in headers:
                    self.cursor.execute(self.alter.format(spider_name=spider.name,columns=i,num=len_num))
            self.first = 2

        str_list = []
        column_list =[]
        for i in item:
            if item[i]:
                column_list.append("`" + i + "`")
                str_list.append("'" + item[i] + "'")
        column = ",".join(column_list)
        values = ",".join(str_list)
        sqltext = self.template.format(spider_name=spider.name,column=column,values=values)
        self.cursor.execute(sqltext)
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