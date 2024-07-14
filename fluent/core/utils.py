# -*- coding: utf-8 -*-
"""工具类

Todo:
    * 将默认值放到配置文件中去实现
"""
import datetime
import inspect
import logging
import os
import sys
import threading
import traceback

import gevent

from fluent import _global
from fluent.utils import sleep

PY2 = sys.version_info[0] == 2
PY3 = sys.version_info[0] == 3


class CatchExceptionHandler:
    """捕获异常凭输出日志

    捕获每一item处理的异常，并打印出堆栈信息

    Raises:
        Exception: 异常
    """

    def handle_item(self, v):
        raise NotImplemented

    def _handle_item(self, v):
        try:
            return self.handle_item(v)
        except Exception as e:
            logging.error(e)
            logging.error(traceback.format_exc())
            return None


class ThreadSafe(object):
    """线程安全基类

    Attributes
        conf: 配置
        threading_counter: 线程数
        rlock: 锁
        EXIT_SIGNAL: 退出信号
    """

    EXIT_SIGNAL = False

    # INTERVAL_DEFAULT = 0.001
    NAME = ''

    def __init__(self, scheduler, conf):
        self.scheduler = scheduler
        self.conf = conf
        self.threading_counter = self.conf.get("threads", 1)
        self.base_threading_counter = self.conf.get("threads", 1)
        self.sem = threading.Semaphore(self.threading_counter)
        self.interval_time = self.conf.get("interval")
        self.need_exit_thread = set()

    def _interval(self):
        if self.interval_time:
            sleep(self.interval_time)

    def report(self, begin):
        end = datetime.datetime.now()
        internal = end - begin
        interval = int(internal.total_seconds() * (10 ** 3))
        self.scheduler.reporter.report_cost(self.NAME, interval)

    def is_flex_thread_alive(self):
        if _global.GEVENT:
            current_thread_name = gevent.getcurrent().name
        else:
            current_thread_name = threading.currentThread().name
        if self.need_exit_thread and current_thread_name in self.need_exit_thread:
            self.need_exit_thread.remove(current_thread_name)
            return False
        return True

    def start_one_thread(self, thread_name, argv):
        if _global.GEVENT:
            from fluent._gevent import start_one_thread as _start_one_thread
            _start_one_thread(self.start, thread_name, *argv)
        else:
            t = threading.Thread(target=self.start, args=argv)
            t.daemon = True
            t.setName(thread_name)
            t.start()

    def start(self, *args, **kwargs):
        raise NotImplemented

    def exit(self):
        """主线程获取退出信号

        多个线程同步设置， 不能简单的使用信号表示线程退出, 超时未推出则强制推出

        抢占当前正在运行程序的信号, 使子线程处于锁定状态

        :param timeout(int): 设置超时时间
        """
        self.EXIT_SIGNAL = True
        for _ in range(self.threading_counter):
            self.sem.acquire()
        for _ in range(self.threading_counter):
            self.sem.release()

    def _start(self):
        self.sem.acquire()

    def _end(self):
        self.sem.release()


def get_class(module, parent_class):
    """获取模块下继承, 递归获取, 如果有继承关系，会加载最后的子节点类

    Args:
        module (object):
        parent_class (cls):

    Raises:
        ModuleNotFoundError: Not find child class of
    """
    final_class = None
    attrs = list(vars(module).values())
    for a in attrs:
        if inspect.isclass(a):
            if a != parent_class and issubclass(a, parent_class):
                final_class = a
                parent_class = final_class
    if final_class is not None:
        return final_class
    if PY2:
        ModuleNotFoundError = ImportError
    raise ModuleNotFoundError("Not find child class of {} in {}".format(parent_class, module.__file__))


def import_by_abspath(module, abspath):
    """以绝对路径的方式导入模块

    Args:
        module: 模块名
        abspath: 绝对路径
    """
    if PY2:
        import imp
        module = imp.load_source(module, abspath)
        return module
    else:
        import importlib
        spec = importlib.util.spec_from_file_location(module, abspath)
        foo = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(foo)
        return foo


def import_module(directory, filename, parent_class):
    """加载job dir下的类

    Args:
        directory (str): job dir
        filename (str): 文件名
        parent_class (type): 基类

    Returns:
        class: 获取job下的类
    """
    abspath = os.path.join(directory, filename)
    module_name = filename[:-3]
    m = import_by_abspath(module_name, abspath)
    return get_class(m, parent_class)
