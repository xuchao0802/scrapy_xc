import requests
from scrapy import selector
import re
url1 = "http://bxjg.circ.gov.cn/tabid/6596/Default.aspx"
headers1 = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Connection": "keep-alive",
            "Host": "bxjg.circ.gov.cn",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36",
            "Cookie": "__jsluid=646a1aa9a5c9269dde7d980b23569a68; .ASPXANONYMOUS=EDRX24NG1QEkAAAAYjMwOThhNjMtZDRiZC00ZmFlLThmMWYtYTY3ZTJmN2QyNmFj0; Hm_lvt_6a2f36cc16bd9d0b01b10c2961b8900c=1558456002,1559044846,1559741649; ASP.NET_SessionId=zo3kjablw1yc5vyvmrc104vu; language_0=zh-CN; COOKIE_USERID=LTE`"
        }
headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Connection": "keep-alive",
            "Cache-Control": "max-age=0",
            "Content-Type": "multipart/form-data; boundary=----WebKitFormBoundaryPyozqDYXEsu048GU",
            "Host": "bxjg.circ.gov.cn",
            "Origin": "http://bxjg.circ.gov.cn",
            "Upgrade-Insecure-Requests": "1",
            "Referer": "http://bxjg.circ.gov.cn/tabid/6596/Default.aspx",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36",
            "Cookie": "__jsluid=646a1aa9a5c9269dde7d980b23569a68; .ASPXANONYMOUS=EDRX24NG1QEkAAAAYjMwOThhNjMtZDRiZC00ZmFlLThmMWYtYTY3ZTJmN2QyNmFj0; Hm_lvt_6a2f36cc16bd9d0b01b10c2961b8900c=1558456002,1559044846,1559741649; ASP.NET_SessionId=zo3kjablw1yc5vyvmrc104vu; language_0=zh-CN; COOKIE_USERID=LTE`"
        }
req1 = requests.get(url1,headers=headers1)
print(req1.headers)
text1 = req1.text
headers1 = req1.headers
html1 = selector.Selector(req1)
viewstate1 = html1.xpath("input[@name='__VIEWSTATE']/@value").get()
print(viewstate1)
data1 = {
    "__EVENTTARGET":"ess$ctr17198$SearchOrganization$lkbSearch",
    "__EVENTARGUMENT": "",
    "__VIEWSTATE": viewstate1,
    "__VIEWSTATEGENERATOR": "CA0B0334",
    "ScrollTop": "",
    "__essVariable": "ess$ctr17198$SearchOrganization$lkbSearch",
    "ess$ctr17198$SearchOrganization$txtComName": "",
    "ess$ctr17198$SearchOrganization$ddlComType": "-1",
    "ess$ctr17198$SearchOrganization$txtOrgDateS": "",
    "ess$ctr17198$SearchOrganization$txtOrgDateE": "",
    "ess$ctr17198$SearchOrganization$ddlState": "-1",
    "ess$ctr17198$SearchOrganization$ddlSW": "-1",
    "ess$ctr17198$SearchOrganization$ddlRegAddr": "-1"
}
res = requests.get('http://www.baidu.com', files=data1)
temp = re.search(r'--(.*)--', res.request.body.decode()).group(1)
data = re.sub(temp.encode(), b'----WebKitFormBoundaryPyozqDYXEsu048GU', res.request.body)
req2 = requests.post(url=url1,data=data,headers=headers)
print(req2.text)