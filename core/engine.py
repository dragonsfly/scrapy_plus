#coding:utf-8

from scrapy_plus.http.request import Request
from scrapy_plus.http.response import Response

from .spider import Spider
from .scheduler import Scheduler
from .downloader import Downloader
from .pipeline import Pipeline
from scrapy_plus.item import Item

from scrapy_plus.middlewares.spider_middlewares import SpiderMiddlewares
from scrapy_plus.middlewares.downloader_middlewares import DownloaderMiddlewares


class Engine(object):

    def __init__(self):
        self.spider = Spider()
        self.scheduler = Scheduler()
        self.downloader = Downloader()
        self.pipeline = Pipeline()
        self.spider_middlewares = SpiderMiddlewares()
        self.downloader_middlewares = DownloaderMiddlewares()

    #设计方法
    def start(self):
        self._start_engine()

    def _start_engine(self):
        # 1. 先构建爬虫发送的第一个请求
        start_request = self.spider.start_request()

        #### 1.1 请求经过爬虫中间件预处理
        start_request = self.spider_middlewares.process_request(start_request)

        # 2. 将请求交给调度器存储
        self.scheduler.add_request(start_request)

        while True:
            # 3. 获取调度器中的请求对象
            request = self.scheduler.get_request()
            if request is None:
                break

            ##### 3.1 将请求经过下载中间件预处理
            request = self.downloader_middlewares.process_request(request)


            # 4. 将请求交给下载器下载，获取响应对象
            response = self.downloader.get_response(request)

            ##### 4.1 将响应经过下载中间件预处理
            response = self.downloader_middlewares.process_response(response)


            # 5. 将响应对象交给spider解析
            result = self.spider.parse(response)

            # 6. 判断解析结果的类型，分别做处理
            if isinstance(result, Request):
                #### 6.1 如果是请求对象，交给爬虫中间件预处理，再添加到请求队列中
                result = self.spider_middlewares.process_request(result)
                self.scheduler.add_request(result)

            elif isinstance(result, Item):
                #### 6.2 如果是Item数据，交给爬虫中间件预处理，再交给管道
                result = self.spider_middlewares.process_item(result)
                self.pipeline.process_item(result)

            else:
                raise Exception("ERROR ：不能处理parse方法返回的数据")






