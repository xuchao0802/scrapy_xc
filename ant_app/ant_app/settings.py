# -*- coding: utf-8 -*-

# Scrapy settings for ant_app project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html
import time

BOT_NAME = 'ant_app'
SPIDER_MODULES = ['ant_app.spiders']
NEWSPIDER_MODULE = 'ant_app.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'ant_app (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 50#并发

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 3#下载延迟三秒
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# ----------- selenium参数配置 -------------
SELENIUM_TIMEOUT = 25           # selenium浏览器的超时时间，单位秒
#LOAD_IMAGE = True               # 是否下载图片
WINDOW_HEIGHT = 900             # 浏览器窗口大小
WINDOW_WIDTH = 900

# Enable or disable spider middlewares爬虫中间件
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'ant_app.middlewares.AntAppSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares下载中间件
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
MY_USER_AGENT = [
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"
]
DOWNLOADER_MIDDLEWARES = {
#    'ant_app.middlewares.AntAppDownloaderMiddleware': 543,
    #'ant_app.middlewares.RandomUserAgentMiddleware':543
    #'ant_app.middlewares.SeleniumMiddleware': 10
}

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
#连接数据库
MYSQL_HOST = 'localhost'
MYSQL_DBNAME = 'crawl_schema'
MYSQL_USER = 'root'
MYSQL_PASSWD = 'imiss968'
ITEM_PIPELINES = {
#    'ant_app.pipelines.AntAppPipeline': 300,
     #'ant_app.pipelines.LoanPipeline': 300,
    'scrapy_redis.pipelines.RedisPipeline': 300
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latenciesRETRY_TIMES
RETRY_ENABLED=False#重试
RETRY_TIMES =3
#RETRY_HTTP_CODECS=#遇到什么网络状态码
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

#log日志记录
LOG_LEVEL = 'DEBUG'
to_day = time.localtime()
log_file_path = 'log/scrapy_{}_{}_{}.log'.format(to_day.tm_year, to_day.tm_mon, to_day.tm_mday)
#LOG_FILE = log_file_path


COMMANDS_MODULE = "ant_app.commands"#将自定义命令加入到scrapy中

#SPIDER_LOADER_CLASS = ""


#reids
SCHEDULER = "scrapy_redis.scheduler.Scheduler"

DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"
REDIS_START_URLS_AS_SET = False
REDIS_HOST = '127.0.0.1'
REDIS_PORT = 6379
REDIS_PARAMS = {
'password': 'imiss968',
}