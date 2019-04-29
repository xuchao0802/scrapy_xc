# baike_mysql.py
import json
import redis
import pymysql

def main():
    # 指定redis数据库信息
    rediscli = redis.StrictRedis(host='127.0.0.1', port=6379, password='imiss968', db=0)
    # 指定mysql数据库
    mysqlcli = pymysql.connect(host='127.0.0.1', user='root', passwd='imiss968', db='crawl_schema', port=3306,
                               charset='utf8')

    mysqlcli.autocommit(True)
    cur = mysqlcli.cursor()
    print(rediscli)
    while True:
        # FIFO模式为 blpop，LIFO模式为 brpop，获取键值
        source, data = rediscli.blpop(["kouzidashi:items"])
        item = json.loads(data)

        #print(item)
        try:
            # 使用cursor()方法获取操作游标

            sql = '''insert into {spider_name}({column})values ({values})'''
            #print(sql)

            str_list = []
            column_list =[]
            for i in item:
                column_list.append("`" + i + "`")
                str_list.append("'" + item[i] + "'")
            column = ",".join(column_list)
            values = ",".join(str_list)
            name = source.decode("utf-8")
            if ":" in name:
                name = name.split(":")[0]
            sqltext = sql.format(spider_name=name,column=column,values=values)


            cur.execute(sqltext)
            #mysqlcli.commit()
            # 关闭本次操作
            #cur.close()
            print("inserted %s" % column_list[0])
        except pymysql.Error as e:
            print("Mysql Error %d: %s" % (e.args[0], e.args[1]))


if __name__ == '__main__':
    main()