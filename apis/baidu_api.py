import requests
import ssl
host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=1lcrorctDt5SpCGAkWaCPHo7&client_secret=NoTTReewWdt4ZQLV5GA87Cr1nYYxYaS8'
request = requests.get(host,headers={'Content-Type':'application/json; charset=UTF-8'})


content = request.text
if (content):
    print(eval(content)["access_token"])