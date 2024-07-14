# -*- coding: utf-8 -*-
"""Processor

处理数据的主流程
为了保持input和output对外接口简单实现，内部逻辑均在这里实现

Todo:
    1. 将一对多的关系改造成yield方法去实现
"""
import datetime
import types

from .utils import ThreadSafe, CatchExceptionHandler
from ..fsignals import FluentSignal


class Processor(ThreadSafe, CatchExceptionHandler):
    """处理数据"""

    NAME = "Processor"

    def __init__(self, scheduler, conf):
        super(Processor, self).__init__(scheduler, conf)
        self.__q = None

    def put(self, v, out_q):
        """ 如果是一对多关系，则需要重写函数.

        因为从队列中获取到数据涉及到锁的问题，因此不在put函数中获取数据

        Args:
            v: 从input队列中获取到的数据
            out_q (queue.Queue): , 产出队列
        """
        # begin = datetime.datetime.now()
        # r = self._handle_item(v)
        # self.report(begin)
        # out_q.put(r)

        begin = datetime.datetime.now()
        r = self._handle_item(v)
        if isinstance(r, types.GeneratorType):
            for g_item in r:
                if g_item is not None:
                    out_q.put(g_item)
                    self.report(begin)
                    begin = datetime.datetime.now()
        else:
            self.report(begin)
            if r is not None:
                out_q.put(r)

    def exit(self):
        for _ in range(self.threading_counter):
            self.__q.put(FluentSignal.QueueStopBlockedSignal)
        super(Processor, self).exit()

    def start(self, int_q, out_q):
        """"""
        self._start()
        self.__q = int_q
        while True:
            if not self.is_flex_thread_alive():
                break
            v = int_q.get()
            if v == FluentSignal.QueueStopBlockedSignal:
                break
            else:
                self.put(v, out_q)
        self._end()

    def _start_one_thead(self, i):
        thread_name = 'processor_{}'.format(i)
        argv = (self.scheduler.q_of_inputer_processor, self.scheduler.q_of_processor_outputer)
        self.start_one_thread(thread_name, argv)

    def exit_one_thread(self, i):
        thread_name = 'processor_{}'.format(i)
        self.need_exit_thread.add(thread_name)

    def start_threads(self):
        for i in range(1, self.base_threading_counter + 1):
            self._start_one_thead(i)
