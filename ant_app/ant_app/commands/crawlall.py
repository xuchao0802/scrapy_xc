from scrapy.utils.project import get_project_settings
import time
from scrapy.commands import ScrapyCommand


class Command(ScrapyCommand):
    requires_project = True

    def syntax(self):
        return '[options]'

    def short_desc(self):
        return 'Runs all of the spiders'

    def run(self, args, opts):
        spider_list = self.crawler_process.spiders.list()#得到该项目下的所有
        #spider_list = ["boss"]
        for name in spider_list:
            self.crawler_process.crawl(name, **opts.__dict__)
        self.crawler_process.start()

