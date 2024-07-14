# -*- coding: utf-8 -*-
"""数据入口

获取外部数据流，传递给processor处理

"""
import datetime
import logging
import traceback
import types

from .utils import ThreadSafe


class Inputer(ThreadSafe):
    """产生数据的地方

    Attributes:
        internal: 内部中断时间，如果避免过快产生数据，可以在配置文件中设置这个值
    """

    NAME = "Inputer"

    def __init__(self, scheduler, conf):
        super(Inputer, self).__init__(scheduler, conf)
        self.loop = self.conf.get("loop", True)

    def __handle_item(self):
        """捕获异常"""
        try:
            return self.handle_item()
        except Exception as e:
            logging.error(e)
            logging.error(traceback.format_exc())
            return None

    def handle_item_result(self, q):
        begin = datetime.datetime.now()
        v = self.__handle_item()
        if isinstance(v, types.GeneratorType):
            for g_item in v:
                if self.EXIT_SIGNAL and not self.loop:
                    # 只有loop等于false需要中断，正常的yield还是全部返回
                    break
                elif g_item is not None:
                    q.put(g_item)
                    self.report(begin)
                    begin = datetime.datetime.now()
        elif v is not None:
            self.report(begin)
            q.put(v)

    def start(self, q):
        """监听队列"""
        self._start()
        if self.loop:
            while True:
                if self.EXIT_SIGNAL:
                    break
                if not self.is_flex_thread_alive():
                    break
                self.handle_item_result(q)
                self._interval()
            self._end()
        else:
            self.handle_item_result(q)
            self._end()
            self.scheduler.e.set()

    def _start_one_thead(self, i):
        thread_name = 'inputer_{}'.format(i)
        argv = (self.scheduler.q_of_inputer_processor,)
        self.start_one_thread(thread_name, argv)

    def start_threads(self):
        for i in range(1, self.base_threading_counter + 1):
            self._start_one_thead(i)

    def exit_one_thread(self, i):
        thread_name = 'inputer_{}'.format(i)
        self.need_exit_thread.add(thread_name)

    def handle_item(self):
        """生成数据的地方，内部要实现一个死循环去产生数据
        """
        raise NotImplemented
