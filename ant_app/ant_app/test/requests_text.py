import requests
url = "https://wx1.sinaimg.cn/mw1024/9d52c073gy1g0r2esv83dj20ia0wdaf5.jpg"
headers = {
    "Host": "wx1.sinaimg.cn",
    "Connection": "keep-alive",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
    "Accept": "image/webp,image/apng,image/*,*/*;q=0.8",
    "Referer": "https://www.mzitu.com/zipai/",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9"
}
req = requests.get(url,headers=headers)
print(req.status_code)
img = req.content
with open("D:/data/image/meizi2019-3-5-1.png","wb") as f:
    f.write(img)
    f.close()

