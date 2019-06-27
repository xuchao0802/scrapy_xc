import asyncio
import pyppeteer
import time
from urllib import parse

async def main(name,**kwargs):
    browser = await pyppeteer.launch({"headless":False})
    page = await browser.newPage()
    await page.setViewport({"width":1366,"height":768})

    browdict = kwargs
    await page.setJavaScriptEnabled(enabled=True)
    if browdict.get("url"):
        url = browdict.get("url")
        await page.goto(browdict["url"])
        if "sj.qq.com/myapp/detail.htm" in url:
            await page.click("a#J_DetIntroShowMore")
            await asyncio.sleep(2)
        png_name = parse.urlparse(url)
        await page.screenshot({'path': '{}.png'.format(png_name.netloc),"fullPage":True})
    await browser.close()

task=[main("task1",url="https://www.baidu.com"),main("task2",url="https://sj.qq.com/myapp/detail.htm?apkName=com.eg.android.AlipayGphone")]

asyncio.get_event_loop().run_until_complete(asyncio.wait(task))