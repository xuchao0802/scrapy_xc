import requests
import json
import time

def get_douban():
    url = "https://movie.douban.com/j/new_search_subjects?sort=S&range=0,10&tags=&start={}"
    headers = {
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
                "Accept-Encoding": "gzip, deflate",
                "Accept-Language": "zh-CN,zh;q=0.9",
                "Connection": "keep-alive",
                "Host": "movie.douban.com",
                "Upgrade-Insecure-Requests": "1",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36"
            }
    num = 200
    data_nlist = []
    for i in range(0,num,20):
        new_url = url.format(i)
        req = requests.get(new_url,headers=headers)
        if req.status_code != 200:
            print("页面状态码不为200，重试")
            time.sleep(6)

            req = requests.get(new_url, headers=headers)
        json_data = json.loads(req.text)
        data = json_data["data"]
        for i in data:
            new_dict = {}
            new_dict["title"] = i.get("title")
            new_dict["rate"] = i.get("rate")
            new_dict["cover"] = i.get("cover")
            data_nlist.append(new_dict)
        time.sleep(2)
        print("等待2秒，进行下一页面爬取")
    with open("ans.json","w") as f:
        json.dump(data_nlist,f)


if __name__ == "__main__":
    get_douban()
    print("爬取完毕")








