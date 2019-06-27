def test():
    zongjia = input("请输入总价：")
    jiage = input("请输入商品价格（中间以空格隔开）:")
    jiage_list = jiage.split(" ")
    try:
        zongjia = int(zongjia)
    except Exception:
        print("总价输入错误")
    try:
        jiage_int = [int(i) for i in jiage_list]

    except Exception:
        print("价格输入错误")
    jiage_int.sort()
    jieguo = 0
    for i in jiage_int:
        jieguo +=i
        if jieguo > zongjia:
            shuchu = jieguo-i
            break
    if max(jiage_int) >10000:
        print("单价超过一万")
    print(shuchu)
def test1():
    data = input("请输入日期：")
    keyword = input("请输入信息:")
    data_list = data.split(" ")
    try:
        data_int = [int(i) for i in data_list]
    except Exception:
        print("日期输入错误")
    fenzu = {
    0:"ABCDEFGHI",
    1:"JKLMNOPQR",
    2:"STUVWXYZ "
    }
    fenzu1 = fenzu[(0-data_int[0]-1)%3]
    fenzu2 = fenzu[(1-data_int[0]-1)%3]
    fenzu3 = fenzu[(2-data_int[0]-1)%3]

    def str_xd(str, num):
        str = str
        str1 = ""
        num = num
        for i in range(len(str)):
            str1 += str[(i + num-1) % len(str)]
        return str1
    fenzu1_new = str_xd(fenzu1,data_int[1])
    fenzu2_new = str_xd(fenzu2,data_int[1])
    fenzu3_new = str_xd(fenzu3,data_int[1])
    dict_fenzunew = {
        1:fenzu1_new,
        2: fenzu2_new,
        3: fenzu3_new,

    }
    list_str = []
    for i in keyword:
        if i not in "ABCDEFGHIJKLMNOPQRSTUVWXYZ ":
            print("信息输入错误")
            break
        for j in dict_fenzunew:
            if i in dict_fenzunew[j]:
                position1 = dict_fenzunew[j].find(i)+1
                position = str(j)+str(position1)
                list_str.append(position)
    print(" ".join(list_str))
test1()









