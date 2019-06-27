# baike_mysql.py
import json
import redis
import pymysql
import time

def main():
    # 指定redis数据库信息
    sql = '''SELECT distinct detail_url FROM crawl_schema.lianjia
    '''
    rediscli = redis.StrictRedis(host='127.0.0.1', port=6379, password='imiss968', db=0)
    # 指定mysql数据库
    mysqlcli = pymysql.connect(host='127.0.0.1', user='root', passwd='imiss968', db='crawl_schema', port=3306,
                               charset='utf8')
    rediscli.hmset("haode",{"name":"xuchao","address":"hangzhou"})
    #mysqlcli.autocommit(True)
    cur = mysqlcli.cursor()
    num = cur.execute(sql)
    for i in range(num):
        data = cur.fetchone()
        url = data[0]
        if url:
            rediscli.lpush("lianjia:start_urls",url)

def redis_test():
    rediscli = redis.StrictRedis(host='127.0.0.1', port=6379, password='imiss968', db=0)
    rediscli.hmset("haode",{"name":"xuchao","address":"hangzhou"})


if __name__ == '__main__':
    time1 = time.time()
    redis_test()
    time2 = time.time()
    print(time2-time1)
