#!/usr/bin/env
# encoding: utf-8
"""
-------------------------------------------------
    date:          2019-11-30   
    Author:       chenzikun         
-------------------------------------------------
工具模块
"""
import logging
import threading
import time
import traceback

import gevent
import socket
from collections import defaultdict

from six.moves import _thread as thread

from fluent import _global


def sleep(s):
    """兼容线程和协成的sleep"""
    if _global.GEVENT == True:
        gevent.sleep(s)
    else:
        time.sleep(s)


class lazyproperty(object):
    """lazy property"""

    def __init__(self, func):
        self.func = func

    def __get__(self, instance, cls):
        if instance is None:
            return self
        else:
            value = self.func(instance)
            setattr(instance, self.func.__name__, value)
            return value


class threadlazyproperty(object):
    """单线程实例property"""
    instances = defaultdict(lambda: defaultdict(dict))

    def __init__(self, func):
        """"""
        self.func = func

    @classmethod
    def clear_thread(cls):
        """弹性线程带来的内存泄漏风险"""
        t_ids = {t.ident for t in threading.enumerate()}
        current_ids = set(cls.instances.keys())
        release_ids = current_ids - t_ids
        if release_ids:
            for ident in release_ids:
                del cls.instances[ident]

    def __get__(self, instance, cls):
        ident = thread.get_ident()
        if cls is None:
            return self
        else:
            if self.func.__name__ in self.instances[ident][instance]:
                return self.instances[ident][instance][self.func.__name__]
            value = self.func(instance)
            self.instances[ident][instance][self.func.__name__] = value
            return value


class threadsingleton(object):
    instances = defaultdict(lambda: defaultdict(dict))

    def __init__(self, cls):
        """"""
        self.cls = cls

    @classmethod
    def clear_thread(cls):
        """弹性线程带来的内存泄漏风险"""
        t_ids = {t.ident for t in threading.enumerate()}
        current_ids = set(cls.instances.keys())
        release_ids = current_ids - t_ids
        if release_ids:
            for ident in release_ids:
                del cls.instances[ident]

    def __call__(self, *args, **kwargs):
        ident = thread.get_ident()
        if str((args, kwargs)) in self.instances[ident][self.cls]:
            return self.instances[ident][self.cls][str((args, kwargs))]
        value = self.cls(*args, **kwargs)
        self.instances[ident][self.cls][str((args, kwargs))] = value
        return value


def catch_gevent_exception(gs):
    for p in gs:
        try:
            _ = p.get()
        except Exception as e:
            logging.error(traceback.format_exc())
            logging.error('catch_gevent_exception: {}'.format(e))
            raise e


def get_host_ip():
    """
    查询本机ip地址
    :return: ip
    """
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip


HOST_IP = get_host_ip()
HOST_NAME = socket.gethostname()
