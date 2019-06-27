import requests
url = "http://www.cbrc.gov.cn/chinese/newListDoc/111003/1.html"
ses = requests.session()
req = ses.get(url=url)
sta = req.status_code
for i in ses.cookies:
    print(i)
print(sta)