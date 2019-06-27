import requests
import threading
from time import time
import json
import re


def downloadFile(URL, spos, epos, fp):
    try:
        header = {}
        header["Range"] = "bytes={}-{}".format(spos, epos)
        result = requests.get(URL, headers=header,verify=False)
        fp.seek(spos)
        fp.write(result.content)
    except Exception:
        print(Exception)


def split_file(file_size):
    start_p = []
    end_p = []
    per_size = int(file_size / thread_num)
    int_size = per_size * thread_num  # 整除部分
    for i in range(0, int_size, per_size):
        start_p.append(i)
        end_p.append(i + per_size - 1)
    if int_size < file_size:  # size 不一定 n 等分，将不能等分余下的部分添加到最后一个 sub 里
        end_p[-1] = file_size
    return start_p, end_p


# 线程数量
thread_num = 30

# 需要填写的变量
url = "https://d11.baidupcs.com/file/d6fcaf9ab6491ebb4431e46d7dc1d60f?bkt=p3-000036a920c908ff1023b546b4384afcbca1&xcode=452d490a85017d4f39a06a106f5bf520039095cf16f1d48f30d7f3776110fac170e5d25e7fb5397b776ecf51471b1f6c316128a2cdfcce4d&fid=795722529-250528-306357153128567&time=1559453674&sign=FDTAXGERLQBHSKf-DCb740ccc5511e5e8fedcff06b081203-wE5pYOZWJL4UC00NUIzUgkvHn1I%3D&to=d11&size=5237491&sta_dx=5237491&sta_cs=2862&sta_ft=mp4&sta_ct=5&sta_mt=4&fm2=MH%2CQingdao%2CAnywhere%2C%2Czhejiang%2Cct&ctime=1552551933&mtime=1557932496&resv0=cdnback&resv1=0&vuk=795722529&iv=0&htype=&newver=1&newfm=1&secfm=1&flow_ver=3&pkey=000036a920c908ff1023b546b4384afcbca1&sl=76480590&expires=8h&rt=pr&r=999382062&mlogid=3538428740060366245&vbdid=3265634929&fin=%E6%9C%BA%E5%99%A8%E5%AD%A6%E4%B9%A0%E4%B9%8B%E6%94%AF%E6%8C%81%E5%90%91%E9%87%8F%E6%9C%BA2.mp4&fn=%E6%9C%BA%E5%99%A8%E5%AD%A6%E4%B9%A0%E4%B9%8B%E6%94%AF%E6%8C%81%E5%90%91%E9%87%8F%E6%9C%BA2.mp4&rtype=1&dp-logid=3538428740060366245&dp-callid=0.1.1&hps=1&tsl=80&csl=80&csign=kfm24o6%2FtweROsBtmgQIdP%2BkZ7I%3D&so=0&ut=6&uter=4&serv=1&uc=482993123&ti=648eaef5c3fa81d1e3edde53921f2ed8c238cc6040e1a347&by=themis"
down_file_name = '机器学习之支持向量机2.mp4'
# 如果该变量不填就会下载到运行程序的目录下
address = 'D:/'  # 记得最后要加斜杠

file = open(address + down_file_name, 'wb')
res = requests.head(url,verify=False)
# 若有单引号替换成双引号
json_data = re.sub('\'', '\"', str(res.headers))
head_dict = json.loads(json_data)
size = int(head_dict['Content-Length'])
start_pos, end_pos = split_file(size)

tmp = []
print('start download...')
t0 = time()
for i in range(0, thread_num):
    t = threading.Thread(
        target=downloadFile,
        args=(
            url,
            start_pos[i],
            end_pos[i],
            file))
    t.setDaemon(True)  # 主进程结束时，线程也随之结束
    t.start()
    tmp.append(t)
for i in tmp:
    i.join()

file.close()
t1 = time()
total_time = t1 - t0
speed = float(size) / (1000 * total_time)
print('total_time:%.2f s' % total_time)
print('speed:%.2f KB/s' % speed)