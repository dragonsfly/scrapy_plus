#coding:utf-8


class Response(object):
    """
    框架内置的响应类，可以创建响应对象，并初始化参数
    """
    def __init__(self, url, status_code, headers, body):
        self.url = url # 响应的url
        self.status_code = status_code # 响应的状态码
        self.headers = headers # 响应报头
        self.body = body # 响应体内容
