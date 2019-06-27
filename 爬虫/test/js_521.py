from urllib import parse

import execjs.runtime_names
import requests
import re
headers = {
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
                "Accept-Encoding": "gzip, deflate, br",
                "Accept-Language": "zh-CN,zh;q=0.9",
                "Connection":"keep-alive",
                "Host": "www.cbrc.gov.cn",
                "Upgrade-Insecure-Requests":"1",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
            }
url = "http://www.cbrc.gov.cn/chinese/newListDoc/111003/1.html"
req = requests.get(url,headers=headers)
str_last = req.text
kong = re.search("</script>.*",str_last).group()
kong_len = len(kong)
kong_b = kong.encode("utf-8")#\x00\x00...
text = str_last.replace("<script>", "")
text = re.sub("</script>.*", "",text)

js_str1 = "function _log(x){ new Function(x); return x;};function getEvalCode(){var result;" + text + "return result;}"
js_str1 = js_str1.replace("eval", "result = _log")
#os.environ["EXECJS_RUNTIME"] = "Node"
na = execjs.runtime_names.Node
node = execjs.get(na)
#a = execjs.eval(js_str1)


z521 = node.compile(js_str1)
js_r1 = z521.call("getEvalCode")
print(js_r1)
pattern = "(\'__jsl_clearance.+)\};"
if  "dc+=cd" in js_r1:
    pattern = "(var cd,dc=\'__jsl_clearance.+)\};"
cookie_code = re.search(pattern,js_r1).group(1)
cookie_code = re.sub("window.headless|window\[.+?\]|window\.[_\w]+","undefined",cookie_code)
var1 = re.search("var ([_\w\d]+?) ?= ?document\.createElement",cookie_code)
if var1:
    var1 = var1.group(1)
    url_parse = parse.urlparse(url)
    host = url_parse.netloc
    repl = "var " + var1 + " = \'" + host + "\'; return"
    cookie_code = re.sub("var ([_\w\d]+?) ?= ?document\.createElement.+?return",repl,cookie_code,1)
cookie_code = "function getCookie(){return " + cookie_code + "}";
z521_1 = node.compile(cookie_code)
cookie = z521_1.call("getCookie")
print(cookie)






