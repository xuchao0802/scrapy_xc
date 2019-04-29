from scrapy.http.response import Response,Request
Request.dont_filter = True


class spider_def():

    def retry(self, response):
        retry_num = 0
        retry = response.meta
        if "retry" in retry.keys():
            retry_num = retry["retry"]
        retry_num += 1
        if retry_num <=3:
            req = response.request
            req.meta["retry"] = retry_num
            req.dont_filter = True
            return req