net start mysql #启动mysql服务
mysql -u root -h localhost -p **** 登入mysql
use 数据库名 

workbench:
PK: Primary Key 主键 
NN: Not Null 非空 
UQ: Unique 唯一 
BIN: Binary 二进制（比text更大） 
UN: Unsigned 无符号数（非负数） 
ZF: Zero Fill 填充零，比如设计列类型为 int(4) ,创建表时输入字段为1， 则自动填充为0001 
AI: Auto Increment 自增
