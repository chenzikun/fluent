#!/usr/bin/env
# encoding: utf-8
"""
-------------------------------------------------
    date:          2021-05-02   
    Author:       chenzikun         
-------------------------------------------------
# 调度器选择
BackgroundScheduler：适用于调度程序在应用程序的后台运行，调用 start后主线程不会阻塞, 默认使用greenlet executor
GeventScheduler：适用于使用 gevent模块的应用程序， 默认使用greenlet executor

# 执行器选择
ThreadPoolExecutor：线程池执行器。
GeventExecutor： Gevent程序执行器。

集成了apsscheluer, 参见
https://apscheduler.readthedocs.io/en/latest/index.html
"""
import datetime
import logging
import sys
import threading

from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR
from fluent import _global
from fluent.abcmeta import ExtensionABC
from fluent.ctx import register_flow
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers.gevent import GeventScheduler
from pytz import utc

from apscheduler.schedulers.base import BaseScheduler

# ----------- 强制使用id -------------- id是上报的必须条件
old_job = BaseScheduler.add_job


def add_job(*args, **kwargs):
    job_id = args[1].__name__
    if 'id' not in kwargs:
        kwargs['id'] = job_id
    return old_job(*args, **kwargs)


BaseScheduler.add_job = add_job


class CronTasKStatus:
    fail = 'fail'
    success = 'success'


@register_flow('crontask')
class CronTask(ExtensionABC):
    """CPU和内存资源监控器，单线程

    Attributes:
        input_item:S

    Args:
        scheduler(Scheduler)
        conf: 配置项

    """
    EXIT_SIGNAL = False
    NAME = 'cron_task'
    PROCESSPOOL_CONF = 'apscheduler.executors.processpool'

    def __init__(self, scheduler, conf):
        self.conf = conf
        self.scheduler = scheduler
        self.measurement = self.conf.get('measurement')
        timezone = self.conf.get('timezone', 'UTC')
        apscheduler_conf = self.conf.get('apscheduler', {})
        if self.PROCESSPOOL_CONF in apscheduler_conf:
            logging.info('not support processpool executor.')
            sys.exit(-1)
        if _global.GEVENT:
            self.apsscheduler = GeventScheduler(apscheduler_conf, timezone=timezone)
        else:
            self.apsscheduler = BackgroundScheduler(apscheduler_conf, timezone=timezone)
        _global.CRON_TASK = self.apsscheduler
        self.rlock = threading.Lock()

    def report(self, status, job_id, interval):
        """获取监控数据并发送数据"""
        fields = {
            'interval': interval
        }
        try:
            self.scheduler.reporter.send(self.measurement, self.NAME, fields, status=status, job_id=job_id)
        except Exception as e:
            logging.error(e)

    def inspect_task(self, event):
        logging.info(event.__dict__)
        interval = int((datetime.datetime.now(utc) - event.scheduled_run_time).total_seconds() * 1000)
        if event.exception:
            status = CronTasKStatus.fail
        else:
            status = CronTasKStatus.success
        job_id = event.job_id
        self.report(status, job_id, interval)

    def start(self):
        """在独立的线程中启动monitor, 由scheduler去控制"""
        self.apsscheduler.add_listener(self.inspect_task, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)
        self.apsscheduler.start()

    def _start(self):
        self.rlock.acquire()

    def _end(self):
        self.rlock.release()

    def exit(self):
        """退出monitor"""
        self.EXIT_SIGNAL = True
        self._start()
        self.apsscheduler.shutdown()
        self._end()
