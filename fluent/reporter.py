#!/usr/bin/env
# encoding: utf-8
"""
-------------------------------------------------
    date:          2021-02-19   
    Author:       chenzikun         
-------------------------------------------------
telegraf上报
"""
import collections
import errno
import logging
import socket
import time
import traceback

import six

from . import _global


class SendMonitorMessageException(Exception):
    """"""


class Telegraf():
    """监控视图上报"""
    def __init__(self, conf, task_name):
        self.task_name = task_name
        self.measurement = ''
        if conf:
            host = conf.get('host', 'localhost')
            port = conf.get('port', 8094)
            measurement = conf.get('measurement')
            self.__udp_cli = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.__host = (host, port)  # telegraf agent port
            self.measurement = measurement
        else:
            self.__udp_cli = None

    def report(self, report_str):
        """上报数据透传给telegraf。
        数据格式：influxdb规范。

        举例：
        joox_cms_backend,service=adb,method=abc,host=1.1.1.1,result=success cost=100 132434567000
        """
        if self.__udp_cli:
            try:
                return self.__udp_cli.sendto(six.b(report_str), self.__host)
            except socket.error as e:
                if e.errno != errno.ECONNRESET:
                    raise

    def report_task_progress(self, measurement, fields, **tags):
        """cost_time: 毫秒"""
        start_time = time.time()
        start_timestamp = int(start_time * 1000000000)
        fields = collections.OrderedDict(fields)
        tags = collections.OrderedDict(tags)
        report_format = "%s," + "=%s,".join(tags.keys()) + "=%s " + '=%s,'.join(fields.keys()) + "=%s %s"
        report_data = [measurement] + list(tags.values()) + list(fields.values()) + [start_timestamp]
        report_str = report_format % tuple(report_data)
        logging.debug(report_str)
        self.report(report_str)

    def send(self, measurement, name, fields, **tags):
        """发送数据"""
        try:
            tags.update(dict(task_name=self.task_name, name=name))
            if _global.ENV:
                tags['env'] = _global.ENV
            if _global.WORKER_NAME:
                tags['worker_name'] = _global.WORKER_NAME
            self.report_task_progress(measurement, fields, **tags)
        except Exception as e:
            logging.error(e)
            logging.error(traceback.format_exc())
            raise SendMonitorMessageException(e)

    def report_cost(self, name, interval):
        self.send(self.measurement, name, {"interval": interval})

    def close(self):
        pass
