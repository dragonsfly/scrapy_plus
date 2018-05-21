#coding:utf-8

from scrapy_plus.http.request import Request
from scrapy_plus.item import Item

class Spider(object):

    start_url = "http://www.baidu.com/"

    def start_request(self):
        return Request(self.start_url)

    def parse(self, response):
        return Item(response.body)
        #return Request(url)
