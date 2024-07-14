# -*- coding: utf-8 -*-
import logging
import socket
import threading
import traceback

import gevent
from fluent import _global

from fluent.core import Processor
from fluent.utils import sleep
# from concurrent.futures import ThreadPoolExecutor
import gevent.pool
import time
import urllib

def test2(i, a):
    # if i == 5:
    #     raise ValueError('test2 error')
    if i==0 and a =='c':
        urllib.urlopen("http://127.0.0.1:5000/")
    # return i
    logging.info('test2: {}, {}'.format(i, a))
    sleep(1)


def catch_gevent_exception(gs):
    for p in gs:
        try:
            _  = p.get()
        except Exception as e:
            logging.error(traceback.format_exc())
            logging.error('catch_gevent_exception: {}'.format(e))
            raise e

def test1(i):
    pool= gevent.pool.Pool(2)
    ss = 'abcd'
    gs = [pool.spawn(test2, i, s) for s in ss]
    gevent.joinall(gs)
    logging.info('test1: {}'.format(i))
    catch_gevent_exception(gs)
    return

def test():
    pool= gevent.pool.Pool(2)
    gs = [pool.spawn(test1, i) for i in range(4)]
    gevent.joinall(gs)
    catch_gevent_exception(gs)
    return

class UserProcessor(Processor):
    """用户自定义处理流程"""

    def __init__(self, s, conf):
        super(UserProcessor, self).__init__(s, conf)
        self.conf = conf

    def handle_item(self, v):
        """处理数据"""
        logging.info(test())
        # if _global.GEVENT:
        #     current_thread_name = gevent.getcurrent().name
        # else:
        #     current_thread_name = threading.currentThread().name
        logging.info('finish v: {}，gevent {}'.format(v, gevent.getcurrent().name))
        logging.info('finish v: {}，threading {}'.format(v, threading.currentThread().name))
        sleep(100)
        return None
        # return v + v
