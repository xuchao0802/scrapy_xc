from scrapy.crawler import CrawlerProcess
from ant_app.spiders.un_ues.wangdai_kouzidashi import KouzidashiSpider
from ant_app.spiders.un_ues.wangdai_onlineloan import OnlineloanSpider

process = CrawlerProcess()
process.crawl(KouzidashiSpider)
process.crawl(OnlineloanSpider)
process.start()