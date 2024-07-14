#!/usr/bin/env
# encoding: utf-8
"""
-------------------------------------------------
    date:          2021-03-10   
    Author:       chenzikun         
-------------------------------------------------

"""
import gc
import logging
import os
import threading

import psutil

from fluent.utils import sleep
from ..abcmeta import ExtensionABC
from ..ctx import register_flow


@register_flow('monitor_resource')
class MonitorResource(ExtensionABC):
    """CPU和内存资源监控器，单线程

    Attributes:
        input_item:

    Args:
        scheduler(Scheduler)
        conf: 配置项

    """
    EXIT_SIGNAL = False
    NAME = 'monitor_resource'

    def __init__(self, scheduler, conf):
        self.conf = conf
        self.scheduler = scheduler
        self.measurement = self.conf.get('measurement')
        self.interval_second = self.conf.get('interval', 1)
        self.mem_max = self.conf.get('mem_max')
        self.p = psutil.Process(os.getpid())
        self.gc_collect = self.conf.get('gc_collect', False)
        self.rlock = threading.Lock()

    def alert(self, mem=None, cpu=None):
        """"""
        if mem and self.mem_max is not None:
            if mem > int(self.mem_max * 1024):
                logging.warning('mem used({}) is larger than max: {}'.format(mem, self.mem_max))
                self.scheduler.e.set()

    def collect(self):
        if self.gc_collect:
            logging.debug('gc.collect')
            gc.collect()

    def monitor(self):
        """获取监控数据并发送数据"""
        self.collect()
        cpu_percent = self.p.cpu_percent()
        mem = self.p.memory_info().rss / 1024 / 1024
        fields = {
            'cpu': cpu_percent,
            'mem': mem
        }
        try:
            logging.debug(fields)
            self.scheduler.reporter.send(self.measurement, self.NAME, fields)
            self.alert(mem, cpu_percent)
        except Exception as e:
            logging.error(e)

    def _interval(self):
        """监控的频率"""
        sleep(self.interval_second)

    def start(self):
        """在独立的线程中启动monitor, 由scheduler去控制"""
        self._start()
        while True:
            if self.EXIT_SIGNAL:
                break
            self._interval()
            self.monitor()
        self._end()

    def _start(self):
        self.rlock.acquire()

    def _end(self):
        self.rlock.release()

    def exit(self):
        """退出monitor"""
        self.EXIT_SIGNAL = True
        # self.rlock.acquire()
        # self.rlock.release()
