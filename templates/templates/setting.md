CONCURRENT_REQUESTS = 32#并发

DOWNLOAD_DELAY = 3#下载延时

COOKIES_ENABLED = False#是否启用cookies

DOWNLOADER_MIDDLEWARES = {#下载中间件
    'templates.middlewares.TemplatesDownloaderMiddleware': 543,
    'templates.middlewares.RandomUserAgentMiddleware': 543,#随机更换au
    # 'templates.middlewares.ProxyDownloaderMiddleware': 400添加代理
    # 'templates.middlewares.SeleniumMiddleware': 10 #将selenium在scrapy中使用
}

ITEM_PIPELINES = {#管道中间件
    #'templates.pipelines.TemplatesPipeline': 300,
    'templates.pipelines.MysqlPipeline': 290,
    'scrapy_redis.pipelines.RedisPipeline': 300,

}

HTTPERROR_ALLOWED_CODES=[] #允许在此列表中的非200状态代码响应

DOWNLOAD_TIMEOUT = 30超时等待时间


SCHEDULER = "scrapy_redis.scheduler.Scheduler"
DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"#用于检测过滤重复的类


