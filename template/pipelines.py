#自建pipelines模板
#创建自定义类
#将类名添加到settings的ITEM_PIPELINES中

#自定义类的可以的一些需求：1、丢弃和改变item的值 2、写入数据库写入json，MongoDB（官文文档中有例子）3、item的重复过滤
from scrapy.exceptions import DropItem


class MubanPipeline(object):

    def __init__(self,setting):
        self.setting = setting#初始化将类中返回的settings赋值给self.settings

    def process_item(self,item,spider):#必须实现的方法,传入项目对项目进行处理
        '''返回包含数据的dict，返回Item （或任何后代类）对象，
        返回Twisted Deferred（文档中有例子）
        或引发 DropItem异常，丢弃后的项目其他管道将不再处理'''
        raise DropItem("这个{}错误了".format(item))
        #return item

    def open_spider(self,spider):#打开蜘蛛的时候调用此方法，无需返回什么
        pass

    def close_spider(self,spider):#关闭蜘蛛的时候调用此方法，无需返回什么
        pass

    @classmethod
    def from_crawler(cls,crawler):
        s = cls(crawler.settings)
        '''Crawler对象提供对所有Scrapy核心组件的访问，如设置和信号'''
        return s#将ceawler中的settings返回到类中,必须返回一个新实例


