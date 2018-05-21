#coding:utf-8

# try:
#     from Queue import Queue
# except ImportError:
#     from queue import Queue
# six可以兼容py2和py3
from six.moves.queue import Queue


class Scheduler(object):
    def __init__(self):
        self.queue = Queue() # 保存请求对象
        self._filter_set = set() # 保存请求指纹（目前是url）


    def add_request(self, request):
        """
        对请求去重，并添加不重复的请求到队列中
        """
        if not self._filter_request(request):
            self.queue.put(request)
            self._filter_set.add(request.url)


    def get_request(self):
        """
        返回队列的请求对象
        """
        try:
            return self.queue.get(False)
        except:
            return None



    def _filter_request(self, request):
        """
        判断是否是重复请求，如果是重复的返回True，否则返回False
        """
        if request.url in self._filter_set:
            return True
        else:
            return False
