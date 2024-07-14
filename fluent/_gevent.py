#!/usr/bin/env
# encoding: utf-8
"""
-------------------------------------------------
    date:          2021-04-21   
    Author:       chenzikun         
-------------------------------------------------

"""
import logging

from gevent import Greenlet

import gevent


def start_one_thread(func, thread_name, *argv, **kwargs):

    gt = Greenlet(func, *argv, **kwargs)
    gt.name = thread_name
    gt.start()


class GeventFomartter(logging.Formatter):
    """将日志里的线程名替换成协成名"""
    def format(self, record):
        if hasattr(gevent.getcurrent(), 'name'):
            record.threadName = gevent.getcurrent().name
        return super(GeventFomartter, self).format(record)
