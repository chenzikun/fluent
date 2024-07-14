# -*- coding: utf-8 -*-
"""监控模块， 单线程
# todo 增加监控
# 1. 通过监控两个队列的长度来判断处理流程的瓶颈在哪里, 前提条件是队列有一定的长度 done
# 2. 通过监控process处理速度来判断整体进度 done
# 3. 记录每个程序，消耗的时间

"""
import logging
import threading
from collections import namedtuple

from fluent.utils import sleep
from ..abcmeta import ExtensionABC
from ..ctx import register_flow

MonitorEnum = namedtuple("MonitorEnum", "used_rate in_counter out_counter")


class MonitorQueue:
    """对队列数据的监控

    Args:
        q(CounterQueue): 被监控的队列
    """
    NAME = ""

    def __init__(self, q):
        self.q = q
        self.last_in = 0
        self.last_out = 0

    def used_rate(self):
        """记录队列使用比例，可以观测是否某个流程在阻塞"""
        return float(self.q.qsize() / self.q.maxsize)

    def in_counter(self):
        """记录某个瞬间counter值"""
        count = self.q.in_counter - self.last_in
        self.last_in = self.q.in_counter
        return count

    def out_counter(self):
        count = self.q.out_counter - self.last_out
        self.last_out = self.q.out_counter
        return count


class InputQueueMonitor(MonitorQueue):
    """监控入口"""
    NAME = "input_q"


class OutputQueueMonitor(MonitorQueue):
    """监控出口"""
    NAME = "output_q"


@register_flow('monitor')
class Monitor(ExtensionABC):
    """监控器，单线程

    Attributes:
        monitor_items(OutputQueueMonitor):

    Args:
        scheduler(Scheduler)
        conf: 配置项
    """
    EXIT_SIGNAL = False

    def __init__(self, scheduler, conf):
        self.conf = conf
        self.monitor_items = [
            InputQueueMonitor(scheduler.q_of_inputer_processor), OutputQueueMonitor(scheduler.q_of_processor_outputer)
        ]
        self.scheduler = scheduler
        self.measurement = self.conf.get('measurement')
        self.interval_second = self.conf.get('interval', 1)
        self.rlock = threading.Lock()

    def monitor(self):
        """获取监控数据并发送数据"""
        for item in self.monitor_items:
            fields_map = {field: getattr(item, field)() for field in MonitorEnum._fields}
            try:
                logging.debug("item: {}, {}".format(item.NAME, fields_map))
                self.scheduler.reporter.send(self.measurement, item.NAME, fields_map)
            except Exception as e:
                logging.error(e)

    def _interval(self):
        """监控的频率"""
        sleep(self.interval_second)

    def start(self):
        """在独立的线程中启动monitor, 由scheduler去控制"""
        self.rlock.acquire()
        while True:
            if self.EXIT_SIGNAL:
                break
            self._interval()
            self.monitor()
        self.rlock.release()

    def exit(self):
        """退出monitor"""
        self.EXIT_SIGNAL = True
        # self.rlock.acquire()
        # self.rlock.release()
