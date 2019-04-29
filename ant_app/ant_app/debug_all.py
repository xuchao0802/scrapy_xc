from scrapy.cmdline import execute
import time
#now = time.time()
# = time.mktime(time.strptime("2019-03-31 03:00:00","%Y-%m-%d %H:%M:%S"))
#n = int(enable_time-now)
#time.sleep(n)
execute("scrapy crawlall".split())