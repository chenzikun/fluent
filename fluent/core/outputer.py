# -*- coding: utf-8 -*-
"""数据出口

用于将结果输出到外部

"""
import datetime

from .utils import ThreadSafe, CatchExceptionHandler
from ..fsignals import FluentSignal


class Outputer(ThreadSafe, CatchExceptionHandler):
    """消费数据"""

    INTERVAL_DEFAULT = 0.001

    NAME = "Outputer"

    def __init__(self, scheduler, conf):
        super(Outputer, self).__init__(scheduler, conf)
        self.__q = None

    def exit(self):
        for _ in range(self.threading_counter):
            self.__q.put(FluentSignal.QueueStopBlockedSignal)
        super(Outputer, self).exit()

    def start(self, q):
        """控制流程， 从队列中获取数据，并处理"""
        self._start()
        self.__q = q
        while True:
            v = q.get()
            if v == FluentSignal.QueueStopBlockedSignal:
                break
            if not self.is_flex_thread_alive():
                break
            elif v is not None:
                # 开始退出
                begin = datetime.datetime.now()
                self._handle_item(v)
                self.report(begin)
            self._interval()
        self._end()

    def handle_item(self, v):
        """将结果输出到外部"""
        raise NotImplemented

    def _start_one_thead(self, i):
        thread_name = 'outputer_{}'.format(i)
        argv = (self.scheduler.q_of_processor_outputer,)
        self.start_one_thread(thread_name, argv)

    def exit_one_thread(self, i):
        thread_name = 'outputer_{}'.format(i)
        self.need_exit_thread.add(thread_name)

    def start_threads(self):
        for i in range(1, self.base_threading_counter + 1):
            self._start_one_thead(i)
