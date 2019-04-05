from scrapy import selector
html_str = '''<table>
    <td>姓名</td><td>年龄</td></tr>
    <td>龙泽啦啦</td><td>23</td></tr>
    <td>餐巾空</td><td>25</td></tr>
</table>'''
html = selector.Selector(text=html_str)
name = html.xpath("/html/body/table/td[2]/text()").get()

from bs4 import BeautifulSoup
soup = BeautifulSoup(html_str,"html5lib")
name1 = soup.select("td")
print(name,"-----")
print((name1))