# -*- coding: utf-8 -*-
"""数据结构

"""
from six.moves import queue
from persistqueue.queue import Queue


class CounterQueueBase(object):
    _q = None

    def __init__(self, *args, **kwargs):
        self.in_counter = 0
        self.out_counter = 0

    def put(self, item, block=True, timeout=None):
        """写数据到队列中, 迭代器放在这里生成会产生计数的问题，因为现在的计数是基于input q的，要么改变计数，要么将迭代器

        支持生成器
        item是否为None的逻辑放到这里， 因为yield None并不为None
        """
        if item is None:
            return
        self.in_counter += 1
        return self._q.put(item, block=block, timeout=timeout)

    def get(self, block=True, timeout=None):
        self.out_counter += 1
        return self._q.get(block=block, timeout=timeout)

    def qsize(self):
        return self._q.qsize()

    @property
    def maxsize(self):
        return self._q.maxsize


class MemQueue(CounterQueueBase):
    """可以计数的队列

    Attributes:
        in_counter(int): 入队列计数器
        in_counter(int): 出队列计数器
    """

    def __init__(self, *args, **kwargs):
        super(MemQueue, self).__init__(*args, **kwargs)
        self._q = queue.Queue(*args, **kwargs)


class PersistQueue(CounterQueueBase):

    def __init__(self, *args, **kwargs):
        super(PersistQueue, self).__init__(*args, **kwargs)
        self._q = Queue(*args, **kwargs)


class Config():
    def __init__(self, config, domain):
        self.config = config
        self.domain_config = config.get(domain) if domain else {}

    def _get(self, item, default=None):
        v = self.domain_config.get(item, default)
        if not v:
            v = self.config.get(item)
        return v

    def __getattr__(self, item):
        """"""
        return self._get(item)

    def __getitem__(self, item):
        """"""
        return self._get(item)

    def get(self, item, default=None):
        """"""
        return self._get(item, default=default)

    def __repr__(self):
        return "{}(domain_config={}, config={})".format(self.__class__.__name__, self.domain_config, self.config)

    def __str__(self):
        return repr(self)


class Extra(object):
    def __init__(self, extra_string):
        if extra_string:
            self.load_extra(extra_string)

    def load_extra(self, extra_string):
        items = extra_string.split(',')
        for item in items:
            k, v = item.split('=')
            setattr(self, k, v)
