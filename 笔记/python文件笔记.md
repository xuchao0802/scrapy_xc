文件行数的获取：
    以 'U' 标志打开文件, 所有的行分割符通过 Python 的输入方法(例#如 read*() )，返回时都会被替换为换行符\n.
    count = len(open("d:/xxx/xxx.xxx).readlines())//将文件读取到一个列表中
    --
    count=-1
    for count, line in enumerate(open(r"d:/data/zhongxinwanka.json",'r',encoding="utf-8")):
        pass
    count+=1
    print(count)//使用循环的方式统计读取行数，一般用循环 
    --
    count=0
    thefile=open("train.data")
    while True:
        buffer=thefile.read(1024*8192)//读取文件中8mb
        if not buffer:
            break
        count+=buffer.count('\n')#统计\n个数
    thefile.close()
    print(count)
    
    