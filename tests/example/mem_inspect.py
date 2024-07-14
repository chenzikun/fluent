#!/usr/bin/env
# encoding: utf-8
"""
-------------------------------------------------
    date:          2021-04-11   
    Author:       chenzikun         
-------------------------------------------------

"""
import datetime
import logging

import objgraph

from fluent.abcmeta import ExtensionABC
from fluent.ctx import register_flow
from fluent.utils import sleep


@register_flow('mem_inspect')
class MemInspect(ExtensionABC):
    """监控器，单线程

    Attributes:
        input_item:

    Args:
        conf: 配置项
        input_q(queue.Queue): 调度器输入队列
        output_q(queue.Queue): 调度器输出队列
    """
    EXIT_SIGNAL = False

    def __init__(self, scheduler, conf):
        self.scheduler = scheduler
        self.conf = conf
        self.file = open(self.conf.get('filepath'), "w+")

    def report(self):
        """获取监控数据并发送数据"""
        self.file.write(str(datetime.datetime.now()).center(50, '=') + '\n')
        objgraph.show_growth(limit=30, file=self.file)
        self.file.flush()


    def _interval(self):
        """监控的频率"""
        i = self.conf.get("interval", 1)
        if i:
            sleep(i)

    def start(self):
        """在独立的线程中启动monitor, 由scheduler去控制"""
        while True:
            if self.EXIT_SIGNAL:
                break
            self.report()
            self._interval()

    def exit(self):
        self.EXIT_SIGNAL = True
        self.file.close()
        logging.info('{} is exit.'.format(self.__class__.__name__))
