#coding:utf-8

import requests
from scrapy_plus.http.response import Response

class Downloader(object):

    def get_response(self, request):
        if request.method.upper() == "GET":
            res = requests.get(
                request.url,
                headers = request.headers,
                params = request.params
            )

        elif request.method.upper() == "POST":
            res = requests.post(
                request.url,
                headers = request.headers,
                params = request.params,  #查询字符串
                data = request.data  # 表单数据
            )
        else:
            raise Exception("ERROR : 不支持该请求方法")

        return Response(
            res.url,
            res.status_code,
            res.headers,
            res.content
        )
