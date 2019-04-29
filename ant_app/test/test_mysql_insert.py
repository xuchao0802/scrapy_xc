import pymysql
create = '''create table if not exists {spider_name}({columns}); '''
column_list = ["`name1`","`name2`","`name3`","`name4`","`name5`","`name6`","`name7`","`name8`"]
column = ",".join(column_list)

template = '''insert into {spider_name}({columns})values ({values});'''
base = "'qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM_1234567890{}:{}'"
host = "localhost"
user = "root"
password = "imiss968"
database = "crawl_schema"
db = pymysql.connect(host=host, user=user, password=password, db=database, port=3306, charset="utf8")
cursor = db.cursor()


db.commit()
for i in range(10000):
    values_list = []
    for j in range(8):
        values_list.append(base.format(j,i))
    values = ",".join(values_list)
    sql1 = template.format(spider_name="test", columns=column,values=values)
    cursor.execute(sql1)
    db.commit()

cursor.close()
db.close()

