# -*- coding: utf-8 -*-
"""
监控模块， 单线程
# todo 增加监控
# 1. 通过监控两个队列的长度来判断处理流程的瓶颈在哪里, 前提条件是队列有一定的长度 done
# 2. 通过监控process处理速度来判断整体进度 done
# 3. 记录每个程序，消耗的时间

"""
import logging
import threading
from fluent.compat import PY2
from fluent.utils import sleep, threadlazyproperty, threadsingleton

from ..abcmeta import ExtensionABC
from ..ctx import register_flow

LOWER_USED_RATE = 0.1
HIGHER_USED_RATE = 0.9


class FlexMethod:
    add = 0
    reduce = 1


class ThreadFlexQueue:
    """对队列数据的监控

    Args:
        q(queue.Queue): 被监控的队列
    """
    NAME = ""

    def __init__(self, q):
        self.q = q

    def used_rate(self):
        """记录队列使用比例，可以观测是否某个流程在阻塞"""
        return float(self.q.qsize() / self.q.maxsize)

    def is_lower_state(self):
        return self.used_rate() < LOWER_USED_RATE

    def is_higher_state(self):
        return self.used_rate() > HIGHER_USED_RATE


class FlowThreadNumberManager():
    """
    etl flow线程管理器

    Attributes:
        flow: etl flow
        base_number: 基础配置线程数
        max_number： 最大线程数
        flex_step: 线程弹性伸缩值
    """
    def __init__(self, flow, flex_max_rate, flex_step_rate):
        self.flow = flow
        self.base_number = self.flow.base_threading_counter
        self.max_number = int(self.base_number * flex_max_rate)
        self.flex_step = int(self.base_number * flex_step_rate) if int(self.base_number * flex_step_rate) >= 1 else 1

    def is_larger_than_base(self):
        return self.flow.threading_counter > self.base_number

    def is_less_than_max_number(self):
        return self.flow.threading_counter < self.max_number

    def get_add_flex_step(self):
        """获取单次增加线程量"""
        if self.flow.threading_counter + self.flex_step > self.max_number:
            return self.max_number - self.flow.threading_counter
        return self.flex_step

    def get_reduce_flex_step(self):
        """获取单次减少线程量"""
        if self.flow.threading_counter <= self.base_number:
            return 0
        if self.flow.threading_counter - self.base_number < self.flex_step:
            return self.flow.threading_counter - self.base_number
        return self.flex_step

    def add(self):
        """减少线程"""
        add_flex_step = self.get_add_flex_step()
        for _ in range(add_flex_step):
            self.flow.threading_counter += 1
            if PY2:
                self.flow.sem._Semaphore__value += 1
            else:
                self.flow.sem._value += 1
            self.flow._start_one_thead(self.flow.threading_counter)

    def reduce(self):
        """增加线程"""
        reduce_flex_step = self.get_reduce_flex_step()
        for _ in range(reduce_flex_step):
            self.flow.exit_one_thread(self.flow.threading_counter)
            self.flow.threading_counter -= 1
            if PY2:
                self.flow.sem._Semaphore__value -= 1
            else:
                self.flow.sem._value -= 1
        self.collect_mem()

    def collect_mem(self):
        threadlazyproperty.clear_thread()
        threadsingleton.clear_thread()


@register_flow('thread_flex')
class ThreadFlex(ExtensionABC):
    """线程弹性伸缩管理器，单线程

    Args:
        scheduler(Scheduler)
        conf: 配置项
    """
    EXIT_SIGNAL = False
    EXIT_PRE = True
    NAME = 'thread_flex'


    def __init__(self, scheduler, conf):
        """

        :param scheduler: Scheduler
        :param conf: 配置
        """
        self.conf = conf
        self.scheduler = scheduler
        self.measurement = self.conf.get('measurement')
        self.interval_second = self.conf.get('interval', 60)

        self.input_q = ThreadFlexQueue(self.scheduler.q_of_inputer_processor)
        self.output_q = ThreadFlexQueue(self.scheduler.q_of_processor_outputer)

        flex_step_rate = self.conf.get('flex_step_rate', 0.1)
        self.input_manager = FlowThreadNumberManager(self.scheduler.input, self.conf.get('input_flex_max_rate', 1),
                                                     flex_step_rate)
        self.processor_manager = FlowThreadNumberManager(self.scheduler.processor,
                                                         self.conf.get('process_flex_max_rate', 1), flex_step_rate)
        self.output_manager = FlowThreadNumberManager(self.scheduler.output, self.conf.get('output_flex_max_rate', 1),
                                                      flex_step_rate)
        self.rlock = threading.Lock()
        self.interval_chunks = self.rerange_interval_chunks()

    def monitor(self):
        """获取监控数据并发送数据"""
        fields_map = {
            'input_counter': self.scheduler.input.threading_counter,
            'processor_counter': self.scheduler.processor.threading_counter,
            'output_counter': self.scheduler.output.threading_counter,
        }
        try:
            logging.debug('threading.active_count:{}'.format(threading.active_count()))
            logging.debug(fields_map)
            self.scheduler.reporter.send(self.measurement, self.NAME, fields_map)
        except Exception as e:
            logging.error(e)

    def rerange_interval_chunks(self):
        INTERVAL_CHUNK = 5
        if self.interval_second <= INTERVAL_CHUNK:
            chunks = [self.interval_second]
        else:
            chunks = [INTERVAL_CHUNK] * int(self.interval_second / INTERVAL_CHUNK)
            if self.interval_second % INTERVAL_CHUNK > 0:
                chunks.append(self.interval_second % INTERVAL_CHUNK)
        return chunks

    def _interval(self):
        """监控的频率"""
        for chunk in self.interval_chunks:
            if not self.EXIT_SIGNAL:
                sleep(chunk)

    def start(self):
        """在独立的线程中启动monitor, 由scheduler去控制"""
        self._start()
        while True:
            if self.EXIT_SIGNAL:
                break
            self.thread_flex_handler()
            self.monitor()
            self._interval()
        self._end()

    def thread_flex_handler(self):
        """线程弹性评估策略模型"""
        if self.input_q.is_lower_state() and self.output_q.is_lower_state():
            if self.input_manager.is_less_than_max_number and self.scheduler.input.loop:
                self.input_manager.add()
            if self.processor_manager.is_larger_than_base():
                self.processor_manager.reduce()
            if self.output_manager.is_larger_than_base():
                self.output_manager.reduce()
        elif self.input_q.is_lower_state() and self.output_q.is_higher_state():
            if self.output_manager.is_less_than_max_number():
                self.output_manager.add()
        elif self.input_q.is_higher_state() and self.output_q.is_lower_state():
            if self.processor_manager.is_less_than_max_number():
                self.processor_manager.add()
        elif self.input_q.is_higher_state() and self.output_q.is_higher_state():
            if self.input_manager.is_larger_than_base() and self.scheduler.input.loop:
                self.input_manager.reduce()
            if self.processor_manager.is_less_than_max_number():
                self.processor_manager.reduce()
            if self.output_manager.is_less_than_max_number():
                self.output_manager.reduce()

    def _start(self):
        self.rlock.acquire()

    def _end(self):
        self.rlock.release()

    def exit(self):
        """退出monitor"""
        self.EXIT_SIGNAL = True
        self._start()
        self._end()